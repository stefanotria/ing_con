# Classe contenente il riconoscitore delle immagini

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, MaxPooling2D
from tensorflow.keras.models import load_model
from PIL import Image
from pathlib import Path
import numpy as np


class Recognition:
    model = ""
    dataset = ""
    epochs = 15

    def __init__(self, dataset):
        self.dataset = dataset
        self.train_data_gen = dataset.generateTrainData()
        self.val_data_gen = dataset.generateTestData()
        self.initializeModel()

    def initializeModel(self):
        my_file = Path("model.h5")
        if my_file.is_file():
            # il file esiste
            self.loadModel("model")
        else:
            self.defineModel()
            self.compileModel()
            self.fitModel()
            self.saveModel("model")

    def defineModel(self):
        self.model = Sequential([
            Conv2D(16, 3, padding='same', activation='relu',
                   input_shape=(self.dataset.IMG_HEIGHT, self.dataset.IMG_WIDTH, 3)),
            MaxPooling2D(),
            Conv2D(32, 3, padding='same', activation='relu'),
            MaxPooling2D(),
            Conv2D(64, 3, padding='same', activation='relu'),
            MaxPooling2D(),
            Flatten(),
            Dense(512, activation='relu'),
            Dense(len(self.dataset.classes), activation='softmax')
        ])

    def compileModel(self):
        self.model.compile(optimizer='adam',
                           loss='categorical_crossentropy',
                           metrics=['accuracy'])

    def fitModel(self):
        total_train = self.train_data_gen.samples
        total_val = self.val_data_gen.samples
        self.model.fit_generator(
            self.train_data_gen,
            steps_per_epoch=total_train // self.dataset.batch_size,
            epochs=self.epochs,
            validation_data=self.val_data_gen,
            validation_steps=total_val // self.dataset.batch_size
        )

    def loadImg(self, filename):
        np_image = Image.open(filename)
        new_image = np_image.resize((self.dataset.IMG_WIDTH, self.dataset.IMG_HEIGHT))
        np_image = np.array(new_image).astype('float32') / 255
        np_image = np_image.reshape((64, 64, 3))
        return np_image

    def predictImages(self):
        sample, _ = next(self.val_data_gen)
        sample_test_images = sample
        total_val = self.val_data_gen.samples
        self.dataset.plotImages(sample_test_images[:total_val], total_val)

        STEP_SIZE_TEST = self.val_data_gen.n // self.dataset.batch_size
        self.val_data_gen.reset()
        pred = self.model.predict_generator(self.val_data_gen,
                                            steps=STEP_SIZE_TEST,
                                            verbose=1)

        predicted_class_indices = np.argmax(pred, axis=1)

        labels = self.train_data_gen.class_indices
        # print(labels)
        labels = dict((v, k) for k, v in labels.items())

        predictions = [labels[k] for k in predicted_class_indices]

        return predictions

    def predictImage(self, image):
        IMAGE_SHAPE = (64, 64)
        image = image.resize(IMAGE_SHAPE)
        img = np.array(image) / 255.0
        result = self.model.predict(img[np.newaxis, ...])
        predicted_class = np.argmax(result[0], axis=-1)

        return predicted_class

    def saveModel(self, nome):
        self.model.save(nome + ".h5")

    def loadModel(self, nome):
        self.model = load_model(nome + ".h5")
