import matplotlib.pyplot as plt
import os
import pandas as pd
from tensorflow.keras.preprocessing.image import ImageDataGenerator

class Dataset:

    PATH = ""
    train_dir = ""
    validation_dir = ""
    IMG_HEIGHT = 64
    IMG_WIDTH = 64

    classes = []

    def __init__(self, batch_size):
        self.PATH = "paintings"
        self.batch_size = batch_size
        for f in os.listdir(os.path.join(self.PATH, 'train')):
            if not f.startswith('.'):
                self.classes.append(f)

    def generateTrainData(self):
        train_dir = os.path.join(self.PATH, 'train')
        train_image_generator = ImageDataGenerator(rescale=1. / 255, horizontal_flip=True)  # Generator for our training data

        train_data_gen = train_image_generator.flow_from_directory(batch_size=self.batch_size,
                                                                        directory=train_dir,
                                                                        shuffle=True,
                                                                        target_size=(self.IMG_HEIGHT, self.IMG_WIDTH),
                                                                        class_mode='categorical')
        return train_data_gen

    def generateTestData(self):
        validation_dir = os.path.join(self.PATH, 'test')
        validation_image_generator = ImageDataGenerator(rescale=1. / 255, horizontal_flip=True)  # Generator for our validation data

        val_data_gen = validation_image_generator.flow_from_directory(batch_size=self.batch_size,
                                                                           directory=validation_dir,
                                                                           target_size=(
                                                                           self.IMG_HEIGHT, self.IMG_WIDTH),
                                                                           class_mode='categorical')
        return val_data_gen

    def getLabelByClass(self, column, index):
        labels = pd.read_csv("label.csv", sep=';')
        label = labels[column].iloc[index]
        print(label)

        return label
