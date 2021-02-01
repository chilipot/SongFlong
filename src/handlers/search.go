package handlers

import (
	"github.com/chilipot/songflong/src/models"
	"github.com/gin-gonic/gin"
	"github.com/zmb3/spotify"
	"net/http"
)

func FindTracks(api *models.ExternalAPI, context *gin.Context) {
	query := context.Query("q")
	resp, err := api.Spotify.Search(query, spotify.SearchTypeTrack)
	if err != nil {
		panic(err)
	}
	if resp.Tracks != nil {
		var tracks []models.Track
		for _, track := range resp.Tracks.Tracks {
			tracks = append(tracks, models.MapToTrack(track))
		}
		context.JSON(http.StatusOK, gin.H{
			"tracks": tracks,
		})
	} else {
		context.JSON(http.StatusOK, gin.H{
			"tracks": []models.Track{},
		})
	}
}
