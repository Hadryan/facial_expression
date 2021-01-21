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
        self.start_button.clicked.connect(self.start)
        self.pause_button.clicked.connect(self.pause)
        self.stop_button.clicked.connect(self.stop)
        self.next_song_button.clicked.connect(self.next_song)
        self.playlist_button.clicked.connect(self.playlist)
        self.YT = None
        self.MP = None
        self.tracks = tracks

    def search_music(self):
        self.YT.is_existed_playlist = False
        playlist = collections.defaultdict(list)
        for name in self.tracks:
            playlist2 = self.YT.search(name)
            playlist = {**playlist, **playlist2}
        self.MP = Music_Player(playlist, maximum=1)
        self.MP.youtube_player()
        self.music_name_label.setText(self.MP.current_music)

    @pyqtSlot()
    def next_song(self):
        if self.MP:
            self.MP.stop_vlc()
            self.MP.next_song()

    @pyqtSlot()
    def playlist(self):
        if self.MP:
            cur, playlist = self.MP.show_playlist()
            if self.MP.is_vlc_playing():
                self.music_name_label.setWordWrap(True)
                self.music_name_label.setText(cur)
                for i, music in enumerate(playlist):
                    if len(music) == 2:
                        self.music_name_label.setText(music[0][:-11])

    @pyqtSlot()
    def start(self):
        if not self.YT:
            self.YT = Youtube_Player(maximum=3)
            self.search_music()

    @pyqtSlot()
    def pause(self):
        if self.MP:
            self.MP.pause_vlc()
            self.music_name_label.setText("Music is paused")

    @pyqtSlot()
    def stop(self):
        if self.MP:
            self.MP.stop_vlc()
            if self.MP.is_vlc_playing():
                self.music_name_label.setText("Music is stopped")
            self.YT = None
            self.MP = None

