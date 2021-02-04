package handlers

import (
	"github.com/chilipot/songflong/src/models"
	"github.com/gin-gonic/gin"
	log "github.com/sirupsen/logrus"
	"github.com/zmb3/spotify"
	"net/http"
	"strconv"
	"sync"
)

type YouTubeStreamURL string

var Itags = map[string][]int{
	"video": {133, 134, 135, 136, 137},
	"audio": {250, 251},
}

type SongBPMResponse struct {
	Songs []struct {
		SongTitle string `json:"song_title"`
		Artist    struct {
			Name string `json:"name"`
		}
	} `json:"tempo"`
}

// Generates an array (max length 5) of songs with a tempo similar or identical
// to the given input value.
func findSongsByTempo(ctx *gin.Context, api *models.ExternalAPI, tempo int) ([]models.SongFlongTrack, error) {
	var songs SongBPMResponse
	var err error
	_, err = api.SongBPM.R().
		SetQueryParams(map[string]string{
			"bpm": strconv.FormatUint(uint64(tempo), 10),
		}).
		ForceContentType("application/json").
		SetResult(&songs).
		Get("/tempo/")
	if err != nil {
		return nil, err
	}
	if len(songs.Songs) == 0 {
		println("No shared BPM songs were found")
		return []models.SongFlongTrack{}, nil
	} else {
		var tracks []models.SongFlongTrack
		for i := 0; i < 5 && i < len(songs.Songs); i++ {
			song := songs.Songs[i]
			track := api.FindTrack(ctx, song.Artist.Name, song.SongTitle)
			tracks = append(tracks, track)
		}
		return tracks, nil
	}
}

// Generic asynchronous handler for fetching the YouTube Stream URL
func getStreamURL(c *gin.Context, api *models.ExternalAPI, youtubeId string, mimeType string) YouTubeStreamURL {
	contextLogger := log.WithFields(map[string]interface{}{"requestID": c.Value("requestID"), "youtubeID": youtubeId, "mimeType": mimeType})
	var streamUrl YouTubeStreamURL
	video, err := api.YouTube.GetVideo(youtubeId)
	if err != nil {
		contextLogger.Error(err)
		return streamUrl
	}
	contextLogger.Debug("found youtube video metadata")

	for _, tag := range Itags[mimeType] {
		format := video.Formats.FindByItag(tag)
		if format == nil {
			continue
		}

		url, err := api.YouTube.GetStreamURLContext(c, video, format)

		if err != nil {
			contextLogger.Error(err)
			break
		}
		contextLogger.Debug("retrieved the stream url")
		streamUrl = YouTubeStreamURL(url)
		break
	}
	contextLogger.Debug("failed to find a stream url")
	return streamUrl
}

// Asynchronously finds the YouTube Stream URLs for both the video and the multiple audio tracks
func getLinks(c *gin.Context, api *models.ExternalAPI, video models.SongFlongTrack, audio []models.SongFlongTrack) (YouTubeStreamURL, []YouTubeStreamURL, error) {
	contextLogger := log.WithField("requestID", c.Value("requestID"))
	var wg sync.WaitGroup
	var videoLink YouTubeStreamURL
	var audioLinks []YouTubeStreamURL

	contextLogger.Debug("spawning the goroutines to retrieve the urls")

	wg.Add(1)
	go func() {
		defer wg.Done()
		link := getStreamURL(c, api, video.GetYouTubeID(), "video")
		videoLink = link
	}()

	for _, track := range audio {
		wg.Add(1)
		go func(track models.SongFlongTrack) {
			defer wg.Done()
			link := getStreamURL(c, api, track.GetYouTubeID(), "audio")
			if link != "" {
				audioLinks = append(audioLinks, link)
			}
		}(track)
	}

	contextLogger.Debug("waiting for goroutines to finish")
	wg.Wait()
	contextLogger.Debug("finished retrieving urls; formatting response")

	return videoLink, audioLinks, nil
}

// Builds the SongFlongTrack from the inputted ID and find other SongFlongTracks with similar tempo.
func getStreamsHandler(api *models.ExternalAPI, c *gin.Context, trackId string) (YouTubeStreamURL, []YouTubeStreamURL, error) {
	var err error
	contextLogger := log.WithFields(map[string]interface{}{
		"requestID": c.Value("requestID"),
		"trackID":   trackId,
	})

	sourceTrack, err := api.GetTrack(c, spotify.ID(trackId))
	if err != nil {
		return "", nil, err
	}
	contextLogger.Info("found source track")

	sharedTracks, err := findSongsByTempo(c, api, sourceTrack.Tempo)
	if err != nil {
		return "", nil, err
	}
	contextLogger.Info("found shared tracks")

	contextLogger.Info("fetching the stream urls")
	return getLinks(c, api, sourceTrack, sharedTracks)
}

// Handles HTTP requests for Streams and responds with the proper links in JSON format.
// Will abort if any errors occur
func GetStreams(api *models.ExternalAPI, c *gin.Context) {
	contextLogger := log.WithField("requestID", c.Value("requestID"))

	trackId := c.Query("id")

	contextLogger.WithField("trackID", trackId).Info("retrieving streams")

	videoLink, audioLinks, err := getStreamsHandler(api, c, trackId)

	if err != nil {
		contextLogger.Error("failed to retrieve streams")
		c.AbortWithError(http.StatusInternalServerError, err)
		return
	}

	contextLogger.Info("successfully retrieved streams")

	c.JSON(http.StatusOK, gin.H{
		"jobId": trackId,
		"video": videoLink,
		"audio": audioLinks,
	})
}
