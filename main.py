import json
import cv2
import csv
import numpy as np
from collections import defaultdict
from keras.models import load_model

#############################################
from face_detection import face_detect
from music_player import Music_Player
from weather import Weather_Api

#############################################

model = load_model('./file/save_model1.h5')

FACE = face_detect("./file/haarcascade_frontalface_alt.xml")  # haarcascade_frontalface_alt path
WTH = Weather_Api()

face_expression = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
face_expression_cnt = defaultdict(int)

cap = cv2.VideoCapture("./file/video.mp4")  # video path

while True:
    success, img = cap.read()
    if not success:
        break
    faces, flag = FACE.detect_face(img)
    for person in faces:
        # cv2.imshow('person', person)
        person = np.asarray(person)
        person = person.astype('float32') / 255.0
        person = np.array([person])
        mood = face_expression[model.predict(person).argmax()]
        face_expression_cnt[mood] += 1
        # cv2.waitKey(1)

    if flag:
        mood = max(face_expression_cnt, key=lambda key: face_expression_cnt[key])
        # ave predicted facial expression as the mood variance.
        with open("./file/data_file.json", 'r', encoding='UTF-8') as file:
            data = json.load(file)

        file = open('exp_weather.csv', 'a', encoding='euc_kr', newline='')
        wr = csv.writer(file)
        current_weather = WTH.get_current_weather()
        current_weather = current_weather.split(' ')[-1]
        wr.writerow(['weather', 'expression'])
        wr.writerow([current_weather])
        file.close()

        choice = input('Current facial expression is %s. Choose one between %s , %s, current weather and exit.: ' % (mood, 'playing music', 'get recommendation'))

        if choice == 'playing music':
            if mood in data['tracks']:
                check = input('Do you want to listen a music? (yes/ or) : ')
                if check.lower() == 'yes':
                    player = Music_Player(data['tracks'], mood=mood)
                    while True:
                        set = input('play / next song / stop) : ')

                        if set.lower() == 'play':
                            player.play_music()
                        elif set.lower() == 'next song':
                            player.stop_music()
                            player.next_song()
                        elif set.lower() == 'stop':
                            if not player.is_music_playing():
                                break
                            player.stop_music()
                            break
        elif choice == 'get recommendation':
            if mood in data['todo']:
                print("Some recommendations for %s" % mood)
                for do in data['todo'][mood]:
                    print(do)
        elif choice == 'current weather':
            print("Current weather is %s." % current_weather)

        flag = False