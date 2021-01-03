# Facial Expression 
Recommend some activities according to facial expression. (ex. 'sad' expression: play a song which make the person feel better)

## System

<center> <img src="https://github.com/sammiee5311/facial_expression/blob/main/file/design.png"> </center>

## How to use
+ download a pre-trained model.
+ change music or options on '.file/data_file.json'
+ write google api key on youtube.py [code](https://github.com/sammiee5311/facial_expression/blob/40c739754e711ad150c283371105b70a867f70f7/youtube.py#L9)
``` python
self.DEVELOPER_KEY = 'API KEY'
```
+ run start_window.py

## How it works
+ detect the face on the pictures or videos in real time by using haarcascade.
+ use a pre-trained model to predict a facial expression with only a face area on the pic.
+ recommend some activities everytime the 'predict' button is clicked.
+ there are two choices
  * play some music
  * show some activities

## Requirments
+ vlc
+ opencv-python
+ tensorflow
+ keras
+ numpy
+ glob
+ pyqt5
+ google-api-python-client
+ pafy

## Reference
https://www.kaggle.com/msambare/fer2013
