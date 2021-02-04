package handlers

import (
	"github.com/chilipot/songflong/src/models"
	"github.com/gin-gonic/gin"
	log "github.com/sirupsen/logrus"
	"github.com/zmb3/spotify"
	"net/http"
)

// Queries the Spotify API to find their data model for the Track
// Converts the spotify.FullTrack to a models.Track representation
func findTracksHandler(api *models.ExternalAPI, c *gin.Context, query string) ([]models.Track, error) {
	var err error
	resp, err := api.Spotify.Search(query, spotify.SearchTypeTrack)
	if err != nil {
		return nil, err
	}
	if resp.Tracks != nil {
		var tracks []models.Track
		for _, track := range resp.Tracks.Tracks {
			tracks = append(tracks, models.MapToTrack(track))
		}
		return tracks, nil
	} else {
		return []models.Track{}, nil
	}
}

// Handles the HTTP requests for searching the Spotify API and responding with the models.Track
// Will abort if any errors occur
func FindTracks(api *models.ExternalAPI, c *gin.Context) {
	contextLogger := log.WithField("requestID", c.Value("requestID"))

	query := c.Query("q")

	contextLogger.WithField("query", query).Info("searching Spotify API")

	tracks, err := findTracksHandler(api, c, query)
	if err != nil {
		contextLogger.Error("failed to search the Spotify API")
		c.AbortWithError(http.StatusInternalServerError, err)
		return
	}

	contextLogger.WithField("tracksLength", len(tracks)).Info("successfully search the Spotify API")

	c.JSON(http.StatusOK, gin.H{
		"tracks": tracks,
	})
}
