package models

import (
	"github.com/zmb3/spotify"
)

type Artist struct {
	Name string     `json:"name"`
	ID   spotify.ID `json:"id"`
}
