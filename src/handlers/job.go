package handlers

import (
	"github.com/chilipot/songflong/src/models"
	"github.com/gin-gonic/gin"
	"github.com/gin-gonic/gin/binding"
	"io"
	"net/http"
	"os"
	"strconv"
)

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

func _download(api *models.ExternalAPI, youtubeId string, mimeType string) {
	video, err := api.YouTube.GetVideo(youtubeId)
	if err != nil {
		panic(err)
	}
	var resp *http.Response
	for _, format := range video.Formats {
		if format.MimeType == mimeType+"/mp4" && format.AudioChannels == 0 {
			resp, err = api.YouTube.GetStream(video, &format)
			if err != nil {
				panic(err)
			}
			break
		}
	}
	if resp == nil {
		return
	}
	defer resp.Body.Close()
	file, err := os.Create(youtubeId + "-" + mimeType + ".mp4")
	if err != nil {
		panic(err)
	}
	defer file.Close()
	_, err = io.Copy(file, resp.Body)
	if err != nil {
		panic(err)
	}
}

func downloadVideoTracks(api *models.ExternalAPI, track models.SongFlongTrack) {
	_download(api, track.ExternalIDs["youtube"], "video")
}

func downloadAudioTracks(api *models.ExternalAPI, tracks []models.SongFlongTrack) {
	for _, track := range tracks {
		_download(api, track.ExternalIDs["youtube"], "audio")
	}
}

func SubmitJob(api *models.ExternalAPI, context *gin.Context) {
	var track models.Track
	err := context.ShouldBindBodyWith(&track, binding.JSON)
	if err != nil {
		panic(err)
	}
	sourceTrack := api.GetTrack(track.ID)
	sharedTracks := findSongsByTempo(api, sourceTrack.Tempo)
	go downloadVideoTracks(api, sourceTrack)
	go downloadAudioTracks(api, sharedTracks)
	context.JSON(http.StatusOK, gin.H{
		"jobId":       track.ID,
		"numOfShared": len(sharedTracks),
	})
}

func GetJob(api *models.ExternalAPI, context *gin.Context) {
	//jobId := context.Param("jobId")
	context.JSON(http.StatusOK, gin.H{})
}
