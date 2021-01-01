import keras
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Activation
from keras.optimizers import Adam
from kerastuner.tuners import RandomSearch
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import numpy as np
import glob
import cv2
from keras.utils import np_utils

path = './data/train/'
dataset = []
labels = []

names = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']

for i, name in enumerate(names):
    print("%d of %d" %(len(names), i+1))
    for i in glob.glob(path+str(name)+'/*.jpg'):
        img = i.split('/')
        img = img[-1].split('\\')
        image = cv2.imread(path+str(name)+'/'+img[-1])
        image = image.astype('float32') / 255.0
        dataset.append(image)
        labels.append(name)

e = LabelEncoder()
e.fit(labels)
labels = e.transform(labels)
labels = np_utils.to_categorical(labels)

### split train, test set ###
X_train, X_test, y_train, y_test = train_test_split(dataset, labels, test_size=0.2, random_state=1)


### make data into numpy array ###
X_train = np.asarray(X_train)
X_test = np.asarray(X_test)


### build sequential model###
def build_model(hp):
    model = keras.models.Sequential()

    model.add(
        Conv2D(hp.Int("input_units", min_value=32, max_value=512, step=32), (3, 3), input_shape=X_train.shape[1:]))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    for i in range(hp.Int("n_layers", min_value=1, max_value=4)): # if there is no step, +1
        model.add(Conv2D(hp.Int("conv_%d_units" % i, min_value=32, max_value=512, step=32), (3, 3)))
        model.add(Activation('relu'))

    model.add(Flatten())

    model.add(Dense(7))
    model.add(Activation("softmax"))

    model.compile(optimizer=Adam(learning_rate=hp.Choice('learning_rate', values=[1e-2, 1e-3, 1e-4])),
                  loss="categorical_crossentropy",
                  metrics=["accuracy"])

    return model


tuner = RandomSearch(
    build_model,
    objective="val_accuracy",
    max_trials=15,  # how many times change the model randomly
    executions_per_trial=1  # how many times to train the model selected
)

tuner.search(x=X_train,
             y=y_train,
             epochs=20,
             batch_size=64,
             validation_data=(X_test, y_test))

best_hps = tuner.get_best_hyperparameters(num_trials=1)[0]  # save hyperparameters when the val_accuracy is highest.


print("The hyperparameter search is complete. The optimal number of units in the first densely-connected layer is %d, "
      "the number of layers is %d and the optimal learning rate for the optimizer is %f." % (
      best_hps.get('input_units'),
      best_hps.get('learning_rate'),
  best_hps.get('n_layers'))) #

model = tuner.hypermodel.build(best_hps) # save the model the best model among best_hps
model.save('save.h5')

model.fit(X_train, y_train, batch_size=64, epochs=5, validation_data = (X_test, y_test))
