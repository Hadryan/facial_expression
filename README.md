# Facial Expression 
Recommend some activities according to facial expression. (ex. 'sad' expression: play a song which make the person feel better)

## how it works
+ detect the face on the pictures or videos in real time by using haarcascade.
+ use a pre-trained model to predict a facial expression with only a face area on the pic.
+ recommend some activities every minute(It depends on the setting).
+ there are three choices
  * play some music
  * show some activities
  * show current weather

## requirments
+ vlc
+ opencv-python
+ tensorflow
+ keras
+ numpy
+ glob

## reference
https://www.kaggle.com/msambare/fer2013
