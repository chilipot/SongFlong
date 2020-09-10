import jsonpickle
import os
from abc import ABC
from dataclasses import dataclass
from typing import List, Union, Tuple

from app.songflong.utils import GetSongBPMAPI, IMVDBAPI

getsongbpm_api = GetSongBPMAPI(os.getenv('GETSONGBPM_API_KEY'))
imvdb_api = IMVDBAPI(os.getenv('IMVDB_API_KEY'))


class BaseModel(ABC):
    def serialize(self):
        return jsonpickle.encode(self, unpicklable=True)

    @classmethod
    def deserialize(cls, obj):
        return jsonpickle.deserialize(obj)


@dataclass
class Album(BaseModel):
    title: str
    img_url: str = None


@dataclass
class Artist(BaseModel):
    name: str
    img_url: str = None


@dataclass
class Video(BaseModel):
    url: str
    img_url: str = None


@dataclass
class Test(BaseModel):
    album: Album
    video: Video
    artist: Artist
    x: List[Artist]


class Song(BaseModel):
    def __init__(self, title: str, artist: Artist = None, _album: Album = None, _bpm: int = None, _imvdb_id: int = None,
                 _getsongbpm_id: str = None, _video: Video = None, _related_songs_by_tempo: List['Song'] = None):
        self.title = title
        self.artist = artist
        self._album = _album
        self._bpm = _bpm
        self._imvdb_id = _imvdb_id
        self._getsongbpm_id = _getsongbpm_id
        self._related_songs_by_tempo = _related_songs_by_tempo
        self._video = _video

    def finish_loading(self):
        if self._imvdb_id is None and self._getsongbpm_id is not None:
            video_search_result = imvdb_api.video_search(self.title)['results'][0]
            result = imvdb_api.video_lookup(video_search_result['id'])
            self._update_from_imvdb(result)
        elif self._getsongbpm_id is None:
            results = getsongbpm_api.song_full_search(self.title, self.artist.name)['search']
            # Prioritize an exact result, then fall back to rely on the search relevancy
            result = next((res for res in results
                           if res['song_title'].lower() == self.title.lower()
                           and res['artist']['name'].lower() == self.artist.name.lower()), results[0])
            self._update_from_getsongbpm(result)

    @classmethod
    def _from_getsongbpm(cls, obj) -> 'Song':
        return Song(title=obj['song_title'],
                    artist=Artist(name=obj['artist']['name'], img_url=obj['artist']['img']),
                    _album=Album(title=obj['album']['title'], img_url=obj['album']['img']),
                    _bpm=int(obj['tempo']),
                    _getsongbpm_id=obj['song_id'])

    @classmethod
    def _get_yt_url(cls, obj):
        youtube_sources = [source for source in obj['sources'] if source['source'] == 'youtube']
        best_source = next((source for source in youtube_sources if source['is_primary']), youtube_sources[0])
        youtube_url = f"https://www.youtube.com/watch?v={best_source['source_data']}"
        return youtube_url

    @classmethod
    def _from_imvdb(cls, obj) -> 'Song':
        return Song(title=obj['song_title'],
                    _imvdb_id=obj['id'],
                    _video=Video(url=cls._get_yt_url(obj), img_url=obj['image']['o']),
                    artist=Artist(name=obj['artists'][0]['name']))

    def _update_from_getsongbpm(self, obj):
        self._getsongbpm_id = obj['song_id']
        self.title = obj['song_title']
        self.artist = Artist(name=obj['artist']['name'], img_url=obj['artist']['img'])
        self._album = Album(title=obj['album']['title'], img_url=obj['album']['img'])
        self._bpm = int(obj['tempo'])

    def _update_from_imvdb(self, obj):
        self._imvdb_id = obj['id']
        self._video = Video(url=self._get_yt_url(obj), img_url=obj['image']['o'])
        if self.artist is None:
            self.artist = Artist(name=obj['artists'][0]['name'])

    @classmethod
    def search(cls, query: Union[str, Tuple[str, str]]) -> List['Song']:
        # Only the first page of search results
        results = []
        converter = cls._from_getsongbpm
        if isinstance(query, str):
            title_results = imvdb_api.video_search(query)
            results = imvdb_api.multi_video_lookup([res['id'] for res in title_results['results']])
            converter = cls._from_imvdb
        elif isinstance(query, tuple):
            song_title, artist_name = query
            results = getsongbpm_api.song_full_search(song_title, artist_name)['search']
            converter = cls._from_getsongbpm

        out = []
        for result in results:
            try:
                out.append(converter(result))
            except Exception as e:
                print(e)
        return out

    @property
    def imvdb_id(self) -> int:
        if self._imvdb_id is None:
            self.finish_loading()
        return self._imvdb_id

    @property
    def getsongbpm_id(self) -> str:
        if self._getsongbpm_id is None:
            self.finish_loading()
        return self._getsongbpm_id

    @property
    def bpm(self) -> int:
        if self._bpm is None:
            self.finish_loading()
        return self._bpm

    @property
    def album(self) -> Album:
        if self._album is None:
            self.finish_loading()
        return self._album

    @property
    def video(self) -> Video:
        if self._video is None:
            self.finish_loading()
        return self._video

    @property
    def related_songs_by_tempo(self) -> List['Song']:
        if self._related_songs_by_tempo is None:
            # Perform specific lazy loading
            results = getsongbpm_api.related_songs_by_tempo(self.bpm)
            self._related_songs_by_tempo = [self._from_getsongbpm(result) for result in results['tempo']]
        return self._related_songs_by_tempo
