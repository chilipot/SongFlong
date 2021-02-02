package models

import (
	"context"
	"fmt"
	"github.com/gin-gonic/gin"
	"github.com/zmb3/spotify"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

type Track struct {
	Artists []Artist   `json:"artists"`
	ID      spotify.ID `json:"id"`
	Name    string     `json:"name"`
	Album   Album      `json:"album"`
}

type SongFlongTrack struct {
	Track
	Tempo       int               `json:"tempo"`
	ExternalIDs map[string]string `json:"external_ids"`
}

func MapToTrack(track spotify.FullTrack) Track {
	var artists []Artist
	for _, artist := range track.Artists {
		artists = append(artists, Artist{
			ID:   artist.ID,
			Name: artist.Name,
		})
	}
	album := Album{
		Name:    track.Album.Name,
		Images:  track.Album.Images,
		Artists: artists,
		ID:      track.Album.ID,
	}
	return Track{
		Artists: artists,
		ID:      track.ID,
		Name:    track.Name,
		Album:   album,
	}
}

// Calls the necessary APIs to build a SongFlongTrack for the given Spotify ID
func (api *ExternalAPI) createTrack(id spotify.ID) SongFlongTrack {
	fullTrack, err := api.Spotify.GetTrack(id)
	if err != nil {
		panic(err)
	}
	audioAnalysis, err := api.Spotify.GetAudioAnalysis(id)
	if err != nil {
		panic(err)
	}
	youtubeId, err := api.findYouTubeID(fullTrack.Artists[0].Name, fullTrack.Name)
	return SongFlongTrack{
		Track:       MapToTrack(*fullTrack),
		Tempo:       int(audioAnalysis.Track.Tempo),
		ExternalIDs: map[string]string{"youtube": youtubeId},
	}
}

// Adds a SongFlongTrack to the Firestore tracks collection
func (api *ExternalAPI) saveTrack(track SongFlongTrack) {
	ctx := context.Background()
	trackRef := api.Firestore.Doc(fmt.Sprintf("Tracks/%s", track.ID))
	_, err := trackRef.Create(ctx, track)
	if err != nil {
		panic(err)
	}
}

// Gets the SongFlongTrack for the given Spotify ID
func (api *ExternalAPI) GetTrack(ctx *gin.Context, id spotify.ID) (SongFlongTrack, error) {
	trackRef := api.Firestore.Doc(fmt.Sprintf("Tracks/%s", id))
	docsnap, err := trackRef.Get(ctx)

	var track SongFlongTrack
	if err != nil {
		if status.Code(err) == codes.NotFound {
			// If a miss, build the SongFlongTrack and add it to the Firestore tracks collection
			track = api.createTrack(id)
			go api.saveTrack(track)
		} else {
			return SongFlongTrack{}, err
		}
	} else {
		if err = docsnap.DataTo(&track); err != nil {
			return SongFlongTrack{}, err
		}
	}
	return track, nil
}

func (api *ExternalAPI) FindTrack(ctx *gin.Context, artist string, title string) SongFlongTrack {
	trackId := api.findSpotifyTrack(artist, title).ID
	res, _ := api.GetTrack(ctx, trackId)
	return res
}

func (track *SongFlongTrack) GetYouTubeID() string {
	return track.ExternalIDs["youtube"]
}
