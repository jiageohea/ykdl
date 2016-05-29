#!/usr/bin/env python
# -*- coding: utf-8 -*-

from you_get.util.match import match1
from you_get.util.html import get_content
from you_get.extractor import VideoExtractor
from you_get.compact import urlencode

import json

class DoubanMusic(VideoExtractor):
    name = 'Douban Music (豆瓣音乐)'

    song_info = {}

    def prepare(self):
        if not self.vid:
            self.vid = match1(self.url, 'sid=(\d+)')

        params = {
            "source" : "",
            "sids" : self.vid,
            "ck" : ""
        }
        form = urlencode(params)
        data = json.loads(get_content('https://music.douban.com/j/artist/playlist', data = bytes(form, 'utf-8')))
        self.song_info = data['songs'][0]

    def extract(self):
        song = self.song_info
        self.title = song['title']
        self.artist = song['artist_name']
        self.stream_types.append('current')
        self.streams['current'] = {'container': 'mp3', 'video_profile': 'current', 'src' : [song['url']], 'size': 0}

    def download_playlist(self, url, param):
        self.param = param
        sids = match1(url, 'sid=([0-9,]+)')

        params = {
            "source" : "",
            "sids" : sids,
            "ck" : ""
        }
        form = urlencode(params)
        data = json.loads(get_content('https://music.douban.com/j/artist/playlist', data = bytes(form, 'utf-8')))

        for s in data['songs']:
           self.song_info = s
           self.download_normal()


site = DoubanMusic()