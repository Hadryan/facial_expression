from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, Qt, QThread, pyqtSignal, QObject, QTimer
from PyQt5 import QtWidgets
import collections

######################################
from youtube import Youtube_Player
from music_player import Music_Player
######################################


class Music_Window(QtWidgets.QMainWindow):
    def __init__(self, tracks):
        super(Music_Window, self).__init__()
        loadUi("./gui/music_window.ui", self)
        self.resume_button.clicked.connect(self.resume)
        self.pause_button.clicked.connect(self.pause)
        self.stop_button.clicked.connect(self.stop)
        self.next_song_button.clicked.connect(self.next_song)
        self.playlist_button.clicked.connect(self.playlist)
        self.YT = Youtube_Player(maximum=3)
        self.MP = None
        self.tracks = tracks
        self.search_music()

    def search_music(self):
        self.YT.is_existed_playlist = False
        playlist = collections.defaultdict(list)
        for name in self.tracks:
            playlist2 = self.YT.search(name)
            playlist = {**playlist, **playlist2}
        self.MP = Music_Player(playlist, maximum=1)
        self.MP.youtube_player()
        self.music_name_label.setText(self.MP.current_music)
        self.music_name_label.adjustSize()

    @pyqtSlot()
    def next_song(self):
        self.MP.stop_vlc()
        self.MP.next_song()

    @pyqtSlot()
    def playlist(self):
        cur, playlist = self.MP.show_playlist()
        self.music_name_label.setWordWrap(True)
        self.music_name_label.setText(cur)
        self.music_name_label.adjustSize()
        for i, music in enumerate(playlist):
            if len(music) == 2:
                self.music_name_label.setText(music[0][:-11])

    @pyqtSlot()
    def resume(self):
        self.MP.play_vlc()
        self.music_name_label.setText(self.MP.current_music)
        self.music_name_label.adjustSize()

    @pyqtSlot()
    def pause(self):
        self.MP.pause_vlc()
        self.music_name_label.setText("Music is paused")
        self.music_name_label.adjustSize()

    @pyqtSlot()
    def stop(self):
        self.MP.stop_vlc()
        self.music_name_label.setText("Music is stopped")
        self.music_name_label.adjustSize()

