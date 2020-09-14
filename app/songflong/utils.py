from abc import ABC
from concurrent import futures
from functools import partial
from typing import Callable, List, Tuple
from urllib.parse import quote_plus

import jsonpickle
import requests
from flask import current_app


class QueueAPI:
    @staticmethod
    def decoded_args_func(func, encoded_args):
        decoded_args = jsonpickle.decode(encoded_args)
        return func(*decoded_args['args'], **decoded_args['kwargs'])

    @classmethod
    def enqueue(cls, func: Callable, *args, **kwargs):
        return current_app.q.enqueue(partial(cls.decoded_args_func, func),
                                     jsonpickle.encode({'args': args, 'kwargs': kwargs}, unpicklable=True))


class UtilityAPI(ABC):
    def __init__(self, base_url):
        self.base_url = base_url

    def inject_in_params(self, in_params):
        return in_params

    def inject_in_headers(self, in_headers):
        return in_headers

    def request(self, url, method='get', params=None, body=None, headers=None, **kwargs):
        """
        Requests wrapper with error handling
        :param url: URL to make request
        :param method: HTTP method to use for request (default: GET)
        :param params: query params for request (optional)
        :param body: request body (optional)
        :param headers: request headers (optional)
        :return: request json result
        """
        result = None
        try:
            params = self.inject_in_params(params or {})
            headers = self.inject_in_headers(headers or {}) or None
            resp = getattr(requests, method)(self.base_url + url, params=params, json=body, headers=headers,
                                             **kwargs)
            resp.raise_for_status()
            result = resp.json()
        except requests.exceptions.HTTPError as e:
            print(e)  # Perform some kind of logging
        except Exception as err:
            print(err)  # Perform some kind of logging
        return result

    def concurrent_requests(self, request_funcs):
        with futures.ThreadPoolExecutor(max_workers=min(10, len(request_funcs))) as executor:
            reqs = [executor.submit(request_func) for request_func in request_funcs]

        return [res.result() for res in reqs]


class GetSongBPMAPI(UtilityAPI):
    def __init__(self, api_key):
        self.api_key = api_key
        super().__init__("https://api.getsongbpm.com")

    def inject_in_params(self, in_params):
        in_params['api_key'] = self.api_key
        return in_params

    def song_search(self, query: str):
        return self.request('/search/', params={'type': 'song', 'lookup': quote_plus(query)})

    def song_full_search(self, song_title, artist_name):
        return self.request('/search/', params={
            'type': 'both',
            'lookup': f"song:{song_title}artist:{artist_name}"
        })

    def multi_song_full_search(self, song_queries: List[Tuple[str, str]]):
        return self.concurrent_requests([
            partial(self.song_full_search, song_title, artist_name)
            for (song_title, artist_name) in song_queries
        ])

    def song_lookup(self, song_id: str):
        return self.request(f'/song/{song_id}')

    def multi_song_lookup(self, song_ids: List[str]):
        return self.concurrent_requests([partial(self.song_lookup, song_id) for song_id in song_ids])

    def related_songs_by_tempo(self, bpm: int):
        return self.request('/tempo/', params={'bpm': bpm})


class IMVDBAPI(UtilityAPI):
    def __init__(self, api_key):
        self.api_key = api_key
        super().__init__("https://imvdb.com/api/v1")

    def inject_in_headers(self, in_headers):
        in_headers["IMVDB-APP-KEY"] = self.api_key
        return in_headers

    def video_search(self, query: str):
        return self.request('/search/videos', params={'q': quote_plus(query)})

    def multi_video_search(self, queries: List[str]):
        return self.concurrent_requests([partial(self.video_search, query) for query in queries])

    def video_lookup(self, video_id: int):
        return self.request(f'/video/{video_id}', params={'include': 'sources'})

    def multi_video_lookup(self, video_ids: List[int]):
        return self.concurrent_requests([partial(self.video_lookup, video_id) for video_id in video_ids])
