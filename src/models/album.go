package models

import (
	"github.com/zmb3/spotify"
)

type Album struct {
	Name    string          `json:"name"`
	Artists []Artist        `json:"artists"`
	ID      spotify.ID      `json:"id"`
	Images  []spotify.Image `json:"images"`
}
