import pafy
import re
from googleapiclient.discovery import build
import collections


class Youtube_Player:
    def __init__(self, maximum=1):
        self.DEVELOPER_KEY = ''
        self.YOUTUBE_API_SERVICE_NAME = 'youtube'
        self.YOUTUBE_API_VERSION = 'v3'
        self.maximum = maximum
        self.is_existed_playlist = False
        self.track_number = 0

    def is_contained_text(self, title):
        for text in title:
            text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', text)
            if text.lower() in ['lyrics','audio']:
                return True
        return False

    def youtube_stream_link(self, playlist, len_of_playlist):
        self.track_number = len_of_playlist
        while self.track_number < len_of_playlist + len(playlist):
            self.track_number += 1
            url = 'https://www.youtube.com/watch?v=' + str(playlist[self.track_number][0][-11:])
            video = pafy.new(url)
            best_audio = video.getbestaudio()
            audio_streaming_link = best_audio.url
            playlist[self.track_number].append(audio_streaming_link)

        return playlist

    def search(self, query, len_of_playlist=0):
        youtube_client = build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION,
                        developerKey=self.DEVELOPER_KEY)

        search_response = youtube_client.search().list(
            q=query,
            part='id, snippet'
        ).execute()

        playlist = collections.defaultdict(list)

        if self.is_existed_playlist:
            pass
        else:
            self.track_number = 0

        for search_result in search_response.get('items', []):
            if search_result['id']['kind'] == 'youtube#video':
                if self.is_contained_text(search_result['snippet']['title'].split()):
                    self.track_number += 1
                    playlist[self.track_number].append('%s %s' % (search_result['snippet']['title'], search_result['id']['videoId']))
                if self.maximum == self.track_number:
                    break

        if len(playlist) != 0:
            audio_streaming_link = self.youtube_stream_link(playlist, len_of_playlist)
            return audio_streaming_link


if __name__ == '__main__':
    y = Youtube_Player()
    y.search(query='toosie')