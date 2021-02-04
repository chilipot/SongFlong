package models

import (
	"cloud.google.com/go/firestore"
	"context"
	"errors"
	"fmt"
	"github.com/go-resty/resty/v2"
	"github.com/kkdai/youtube/v2"
	"github.com/zmb3/spotify"
	"golang.org/x/oauth2/clientcredentials"
	"google.golang.org/api/option"
	"log"
	"os"
	"strconv"
)

type ExternalAPI struct {
	Spotify   *spotify.Client
	Imvdb     *resty.Client
	SongBPM   *resty.Client
	Firestore *firestore.Client
	YouTube   *youtube.Client
}

type YouTubeID = string
type MusicVideoID = int // ID used by IMVDB

const IMVDB_API_HOST = "https://imvdb.com/api/v1"
const SONG_BPM_API = "https://api.getsongbpm.com"

// Returns a Client-authenticated Spotify Client
func getSpotifyClient() spotify.Client {
	config := &clientcredentials.Config{
		ClientID:     os.Getenv("SPOTIFY_CLIENT_ID"),
		ClientSecret: os.Getenv("SPOTIFY_CLIENT_SECRET"),
		TokenURL:     spotify.TokenURL,
	}
	token, err := config.Token(context.Background())
	if err != nil {
		log.Fatalf("couldn't get token: %v", err)
	}

	return spotify.Authenticator{}.NewClient(token)
}

func getFireStoreClient() *firestore.Client {
	opt := option.WithCredentialsFile(os.Getenv("GOOGLE_SERVICE_KEY"))
	ctx := context.Background()
	client, err := firestore.NewClient(ctx, "songflong-b0388", opt)
	if err != nil {
		panic(err)
	}
	return client
}

func InitializeSources() ExternalAPI {
	imvdb_api_key := os.Getenv("IMVDB_API_KEY")
	songbpm_api_key := os.Getenv("GETSONGBPM_API_KEY")
	spotClient := getSpotifyClient()
	ytClient := youtube.Client{Debug: true}
	return ExternalAPI{
		Spotify:   &spotClient,
		Imvdb:     resty.New().SetHostURL(IMVDB_API_HOST).SetHeader("IMVDB-APP-KEY", imvdb_api_key),
		SongBPM:   resty.New().SetHostURL(SONG_BPM_API).SetQueryParam("api_key", songbpm_api_key),
		Firestore: getFireStoreClient(),
		YouTube:   &ytClient,
	}
}

type VideoSearchResults struct {
	Results []struct {
		Id int `json:"id"`
	} `json:"results"`
}

type SourceData struct {
	Sources []struct {
		Source     string `json:"source"`
		SourceData string `json:"source_data"`
	}
}

// Finds the IMVDB ID for a music video matching the given artist and song
func (api *ExternalAPI) findVideoId(artist string, title string) MusicVideoID {
	var searchResults VideoSearchResults
	_, err := api.Imvdb.R().
		SetQueryParam("q", artist+" "+title).
		SetResult(&searchResults).
		Get("/search/videos")
	if err != nil {
		panic(err)
	}
	return searchResults.Results[0].Id
}

// Maps the IMVDB ID to a YouTube Video ID
func (api *ExternalAPI) getYouTubeLink(videoId MusicVideoID) (YouTubeID, error) {
	var sourceData SourceData
	_, err := api.Imvdb.R().
		SetQueryParam("include", "sources").
		SetPathParam("videoId", strconv.Itoa(videoId)).
		SetResult(&sourceData).
		Get("/video/{videoId}")
	if err != nil {
		panic(err)
	}
	for i := range sourceData.Sources {
		if sourceData.Sources[i].Source == "youtube" {
			return sourceData.Sources[i].SourceData, nil
		}
	}
	return "", errors.New("no_video_id")
}

func (api *ExternalAPI) findSpotifyTrack(artist string, title string) spotify.FullTrack {
	resp, err := api.Spotify.Search(fmt.Sprintf("%s artist:%s", title, artist),
		spotify.SearchTypeTrack)
	if err != nil {
		panic(err)
	}
	if resp.Tracks != nil {
		return resp.Tracks.Tracks[0]
	} else {
		return spotify.FullTrack{}
	}
}

func (api *ExternalAPI) findYouTubeID(artist string, title string) (YouTubeID, error) {
	mvId := api.findVideoId(artist, title)
	return api.getYouTubeLink(mvId)
}
