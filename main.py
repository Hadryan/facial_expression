from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, Qt, QThread, pyqtSignal, QObject
from PyQt5 import QtWidgets
import threading
import json
import cv2
import csv
import numpy as np
from collections import defaultdict
from keras.models import load_model

#####################################
from music_window import Music_Window
from face_detection import face_detect
######################################


class Webcam(threading.Thread):
    def __init__(self):
        super(Webcam, self).__init__()
        self._stop_event = threading.Event()
        self.is_running = True
        self.model = load_model('save_model1.h5')

        self.FACE = face_detect("./file/haarcascade_frontalface_alt.xml")  # haarcascade_frontalface_alt path
        self.face_expression = ['angry', 'disgust', 'scary', 'happy', 'neutral', 'sad', 'surprise']
        self.face_expression_cnt = defaultdict(int)
        self.mood = 'None'

    def get_facial_expression(self):
        if self.face_expression_cnt:
            self.mood = max(self.face_expression_cnt, key=lambda key: self.face_expression_cnt[key])
        self.face_expression_cnt = defaultdict(int)
        return self.mood

    def stop(self):
        self._stop_event.set()

    def run(self):
        while not self._stop_event.is_set():
            cap = cv2.VideoCapture(0)
            if self.is_running:
                while True:
                    if not self.is_running:
                        break
                    _, img = cap.read()
                    faces = self.FACE.detect_face(img)
                    for person in faces:
                        person = np.asarray(person)
                        person = person.astype('float32') / 255.0
                        person = np.array([person])
                        mood = self.face_expression[self.model.predict(person).argmax()]
                        self.face_expression_cnt[mood] += 1

                    cv2.imshow("img", img)
                    cv2.waitKey(1)


class Main_Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main_Window, self).__init__()
        loadUi("./gui/main_window.ui", self)
        self.youtube_button.clicked.connect(self.start_youtube_music)
        self.webcam_button.clicked.connect(self.start_webcam)
        self.predict_button.clicked.connect(self.get_prediction)
        self.activities_button.clicked.connect(self.get_recommended_activities)
        self.input = self.findChild(QtWidgets.QLineEdit, 'chat_input_label')
        self.mood = None
        self.wc = Webcam()
        self.wc.daemon = True
        self.music_window = None
        self.webcam_window = False
        self.current_statue = None
        with open("./file/data_file.json", 'r', encoding='UTF-8') as file:
            self.data = json.load(file)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        elif e.key() in [Qt.Key_Return, Qt.Key_Enter]:
            if not self.current_statue:
                self.print_chatting()
            else:
                return True

    @pyqtSlot()
    def start_youtube_music(self):
        self.chat_output_label.setText('starting youtube music')
        if not self.music_window and self.mood:
            if self.mood in self.data['tracks']:
                self.music_window = Music_Window(self.data['tracks'][self.mood])
        if self.mood:
            self.music_window.show()
        else:
            self.chat_output_label.setText('Please, predict your facial expression first.')

    @pyqtSlot()
    def get_prediction(self):
        self.mood = self.wc.get_facial_expression()
        self.chat_output_label.setText("Current mood is " + self.mood)
        self.mood_label.setText(self.mood)

    @pyqtSlot()
    def start_webcam(self):
        if not self.webcam_window:
            if not self.wc.is_running:
                self.wc.is_running = True
            else:
                self.wc.start()
        else:
            self.chat_output_label.setText("Webcam is already started.")
        self.webcam_window = True

    def get_recommended_activities(self):
        if self.mood and self.mood in self.data['todo']:
            text = ''
            for todo in self.data['todo'][self.mood]:
                text += todo + ', '
            self.chat_output_label.setText("Recommended activities are " + text)
        else:
            self.chat_output_label.setText("Please, predict your facial expression first.")

    @pyqtSlot()
    def print_chatting(self):
        text = self.input.text()
        if text.lower() == 'activities':
            self.get_recommended_activities()
        elif text.lower() == 'predict':
            self.get_prediction()
        elif text.lower() == 'youtube music':
            self.start_youtube_music()
        elif text.lower() == 'webcam':
            self.start_webcam()
        elif text.lower() == 'exit music':
            self.music_window.close()
        else:
            self.chat_output_label.setText("This command is not in the list")
        self.input.clear()
