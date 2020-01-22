# Classe contenente il riconoscitore delle immagini

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import os
import numpy as np
import matplotlib.pyplot as plt

class Recognition:

    def __init__(self):
        self.total_val = 0
        self.total_train = 0
        self.batch_size = 6
        self.epochs = 15
        self.IMG_HEIGHT = 64
        self.IMG_WIDTH = 64

    def loadDataset(self):
        PATH = 'paintings'

        train_dir = os.path.join(PATH, 'train')
        validation_dir = os.path.join(PATH, 'test')

        self.classes = os.listdir(os.path.join(PATH, 'train'))

        for n in self.classes:
            self.total_train += len(os.listdir(os.path.join(train_dir, n)))
        for n in self.classes:
            self.total_val += len(os.listdir(os.path.join(validation_dir, n)))

        self.generateTrainData(train_dir)
        self.generateTestData(validation_dir)

    def generateTrainData(self, train_dir):
        train_image_generator = ImageDataGenerator(rescale=1. / 255)  # Generator for our training data

        self.train_data_gen = train_image_generator.flow_from_directory(batch_size=self.batch_size,
                                                                        directory=train_dir,
                                                                        shuffle=True,
                                                                        target_size=(self.IMG_HEIGHT, self.IMG_WIDTH),
                                                                        class_mode='categorical')
        sample, _ = next(self.train_data_gen)
        # plotImages(sample_training_images[:5])

    def generateTestData(self, validation_dir):
        validation_image_generator = ImageDataGenerator(rescale=1. / 255)  # Generator for our validation data

        self.val_data_gen = validation_image_generator.flow_from_directory(batch_size=self.batch_size,
                                                                           directory=validation_dir,
                                                                           target_size=(
                                                                           self.IMG_HEIGHT, self.IMG_WIDTH),
                                                                           class_mode='categorical')
        sample, _ = next(self.val_data_gen)

        self.sample_test_images = sample

    def defineModel(self):
        model = Sequential([
            Conv2D(16, 3, padding='same', activation='relu', input_shape=(self.IMG_HEIGHT, self.IMG_WIDTH, 3)),
            MaxPooling2D(),
            Conv2D(32, 3, padding='same', activation='relu'),
            MaxPooling2D(),
            Conv2D(64, 3, padding='same', activation='relu'),
            MaxPooling2D(),
            Flatten(),
            Dense(512, activation='relu'),
            Dense(len(self.classes), activation='softmax')
        ])

        model.compile(optimizer='adam',
                      loss='binary_crossentropy',
                      metrics=['accuracy'])

        history = model.fit_generator(
            self.train_data_gen,
            steps_per_epoch=self.total_train // self.batch_size,
            epochs=self.epochs,
            validation_data=self.val_data_gen,
            validation_steps=self.total_val // self.batch_size
        )

        return model

    def predictImages(self, model):
        self.plotImages(self.sample_test_images[:self.total_val])

        STEP_SIZE_TEST = self.val_data_gen.n // self.val_data_gen.batch_size
        self.val_data_gen.reset()
        pred = model.predict(self.val_data_gen,
                                       steps=STEP_SIZE_TEST,
                                       verbose=1)

        predicted_class_indices = np.argmax(pred, axis=1)

        labels = self.train_data_gen.class_indices
        #print(labels)
        labels = dict((v, k) for k, v in labels.items())

        predictions = [labels[k] for k in predicted_class_indices]

        return predictions

    def plotImages(self, images_arr):
        fig, axes = plt.subplots(1, self.total_val, figsize=(7, 7))
        axes = axes.flatten()
        for img, ax in zip(images_arr, axes):
            ax.imshow(img)
            ax.axis('off')
        plt.tight_layout()
        plt.show()
