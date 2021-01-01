import cv2
import time


class face_detect:
    def __init__(self, path):
        self.base_time = int(time.strftime('%c', time.localtime(time.time()))[-7:-5])
        self.current_time = None
        self.cascade = cv2.CascadeClassifier(path)

    def extract_face(self, img, x, y, w, h):
        img = img[y:y + h, x:x + w, :] # crop the image by using coordinates of x,y,w,h
        img = cv2.resize(img, (48,48))
        return img

    # read cascade file
    def load_cascade_file_n_coordinate(self,gray_img):
        face_list = self.cascade.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=1, minSize=(150, 150))
        return face_list

    def detect_face(self,image_file):
        flag = False
        self.current_time = int(time.strftime('%c', time.localtime(time.time()))[-7:-5])
        people = []
        gray_img = cv2.cvtColor(image_file, cv2.COLOR_BGR2GRAY) # change image to gray color
        face_list = self.load_cascade_file_n_coordinate(gray_img)
        if abs(self.base_time - self.current_time) % 10 == 0 and abs(self.base_time - self.current_time) != 0:
            flag = True
        if len(face_list) > 0:
            for face in face_list:
                x, y, w, h = face
                face_img = self.extract_face(image_file,x,y,w,h)
                cv2.rectangle(image_file, (x, y), (x + w, y + h), (0, 255, 0), 3)
                cv2.imshow('img',image_file)
                cv2.waitKey(1)
                people.append(face_img)

        else:
            print("no face")

        return people, flag


if __name__ == '__main__':
    face = face_detect("./file/haarcascade_frontalface_alt.xml")
    # face.detect_face()
