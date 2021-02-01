package handlers

import (
	"context"
	"github.com/chilipot/songflong/src/models"
	"github.com/gin-gonic/gin"
	"github.com/zmb3/spotify"
	"net/http"
	"strconv"
)

var Itags = map[string][]int{
	"video": {133, 134, 135, 136, 137},
	"audio": {139, 140, 141},
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
func findSongsByTempo(api *models.ExternalAPI, tempo int) []models.SongFlongTrack {
	var songs SongBPMResponse
	_, err := api.SongBPM.R().
		SetQueryParams(map[string]string{
			"bpm": strconv.FormatUint(uint64(tempo), 10),
		}).
		ForceContentType("application/json").
		SetResult(&songs).
		Get("/tempo/")
	if err != nil {
		panic(err)
	}
	if len(songs.Songs) == 0 {
		println("No shared BPM songs were found")
		return []models.SongFlongTrack{}
	} else {
		var tracks []models.SongFlongTrack
		for i := 0; i < 5 && i < len(songs.Songs); i++ {
			song := songs.Songs[i]
			track := api.FindTrack(song.Artist.Name, song.SongTitle)
			tracks = append(tracks, track)
		}
		return tracks
	}
}

func getStreamURL(api *models.ExternalAPI, youtubeId string, mimeType string) string {
	ctx := context.Background()
	video, err := api.YouTube.GetVideo(youtubeId)
	if err != nil {
		panic(err)
	}

	for _, tag := range Itags[mimeType] {
		format := video.Formats.FindByItag(tag)
		if format == nil {
			continue
		}

		url, err := api.YouTube.GetStreamURLContext(ctx, video, format)

		if err != nil {
			panic(err)
		}
		return url
	}
	return ""
}

func getVideoLinks(api *models.ExternalAPI, track models.SongFlongTrack) string {
	return getStreamURL(api, track.ExternalIDs["youtube"], "video")
}

func getAudioLinks(api *models.ExternalAPI, tracks []models.SongFlongTrack) []string {
	var streams []string
	for _, track := range tracks {
		stream := getStreamURL(api, track.ExternalIDs["youtube"], "audio")
		streams = append(streams, stream)
	}
	return streams
}

func GetStreams(api *models.ExternalAPI, context *gin.Context) {
	var track models.Track
	trackId := context.Query("id")
	sourceTrack := api.GetTrack(spotify.ID(trackId))
	sharedTracks := findSongsByTempo(api, sourceTrack.Tempo)
	videoLink := getVideoLinks(api, sourceTrack)
	audioLinks := getAudioLinks(api, sharedTracks)
	context.JSON(http.StatusOK, gin.H{
		"jobId": track.ID,
		"video": videoLink,
		"audio": audioLinks,
	})
}
