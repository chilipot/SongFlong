package handlers

import (
	"context"
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
func getStreamURL(ch chan YouTubeStreamURL, wg *sync.WaitGroup, api *models.ExternalAPI, youtubeId string, mimeType string) {
	ctx := context.Background()
	video, err := api.YouTube.GetVideo(youtubeId)
	if err != nil {
		wg.Done()
		return
	}

	for tag := range Itags[mimeType] {
		format := video.Formats.FindByItag(tag)
		if format == nil {
			continue
		}

		url, err := api.YouTube.GetStreamURLContext(ctx, video, format)

		if err != nil {
			wg.Done()
			return
		}
		ch <- YouTubeStreamURL(url)
		break
	}
	wg.Done()
}

// Asynchronously finds the YouTube Stream URLs for both the video and the multiple audio tracks
func getLinks(api *models.ExternalAPI, video models.SongFlongTrack, audio []models.SongFlongTrack) (YouTubeStreamURL, []YouTubeStreamURL, error) {
	var wg sync.WaitGroup
	videoChan := make(chan YouTubeStreamURL)
	audioChan := make(chan YouTubeStreamURL)

	wg.Add(1)
	go getStreamURL(videoChan, &wg, api, video.GetYouTubeID(), "video")
	for _, track := range audio {
		wg.Add(1)
		go getStreamURL(audioChan, &wg, api, track.GetYouTubeID(), "audio")
	}

	go func() {
		wg.Wait()
		close(videoChan)
		close(audioChan)
	}()

	var audioLinks []YouTubeStreamURL
	for val := range audioChan {
		audioLinks = append(audioLinks, val)
	}

	return <-videoChan, audioLinks, nil
}

// Builds the SongFlongTrack from the inputted ID and find other SongFlongTracks with similar tempo.
func getStreamsHandler(api *models.ExternalAPI, c *gin.Context) (YouTubeStreamURL, []YouTubeStreamURL, error) {
	var err error
	trackId := c.GetString("trackID")

	sourceTrack, err := api.GetTrack(c, spotify.ID(trackId))
	if err != nil {
		return "", nil, err
	}
	sharedTracks, err := findSongsByTempo(c, api, sourceTrack.Tempo)
	if err != nil {
		return "", nil, err
	}
	return getLinks(api, sourceTrack, sharedTracks)
}

// Handles HTTP requests for Streams and responds with the proper links in JSON format.
// Will abort if any errors occur
func GetStreams(api *models.ExternalAPI, c *gin.Context) {
	contextLogger := log.WithField("requestID", c.Value("requestID"))
	contextLogger.Info("retrieving streams")

	trackId := c.Query("id")
	c.Set("trackID", trackId)

	videoLink, audioLinks, err := getStreamsHandler(api, c)

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
