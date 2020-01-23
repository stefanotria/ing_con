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
        #self.classes = os.listdir(os.path.join(self.PATH, 'train'))

        for f in os.listdir(os.path.join(self.PATH, 'train')):
            if not f.startswith('.'):
                self.classes.append(f)

    def plotImages(self, images_arr, total_val):
        fig, axes = plt.subplots(1, total_val, figsize=(7, 7))
        axes = axes.flatten()
        for img, ax in zip(images_arr, axes):
            ax.imshow(img)
            ax.axis('off')
        plt.tight_layout()
        plt.show()

    def generateTrainData(self):
        train_dir = os.path.join(self.PATH, 'train')
        train_image_generator = ImageDataGenerator(rescale=1. / 255)  # Generator for our training data

        train_data_gen = train_image_generator.flow_from_directory(batch_size=self.batch_size,
                                                                        directory=train_dir,
                                                                        shuffle=True,
                                                                        target_size=(self.IMG_HEIGHT, self.IMG_WIDTH),
                                                                        class_mode='categorical')
        return train_data_gen

    def generateTestData(self):
        validation_dir = os.path.join(self.PATH, 'test')
        validation_image_generator = ImageDataGenerator(rescale=1. / 255)  # Generator for our validation data

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
