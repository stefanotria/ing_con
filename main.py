import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import os
import numpy as np
import matplotlib.pyplot as plt

PATH = 'dataset'

train_dir = os.path.join(PATH, 'train')
validation_dir = os.path.join(PATH, 'test')

classes = os.listdir(os.path.join(PATH, 'train'))
total_train = 0
total_val = 0

for n in classes:
    total_train += len(os.listdir(os.path.join(train_dir, n)))
for n in classes:
    total_val += len(os.listdir(os.path.join(validation_dir, n)))

batch_size = 5
epochs = 15
IMG_HEIGHT = 64
IMG_WIDTH = 64

train_image_generator = ImageDataGenerator(rescale=1. / 255)  # Generator for our training data
validation_image_generator = ImageDataGenerator(rescale=1. / 255)  # Generator for our validation data

train_data_gen = train_image_generator.flow_from_directory(batch_size=batch_size,
                                                           directory=train_dir,
                                                           shuffle=True,
                                                           target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                           class_mode='categorical')

val_data_gen = validation_image_generator.flow_from_directory(batch_size=batch_size,
                                                              directory=validation_dir,
                                                              target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                              class_mode='categorical')

sample_training_images, _ = next(train_data_gen)
sample_test_images, _ = next(val_data_gen)


# This function will plot images in the form of a grid with 1 row and 5 columns where images are placed in each column.
def plotImages(images_arr):
    fig, axes = plt.subplots(1, 5, figsize=(7, 7))
    axes = axes.flatten()
    for img, ax in zip(images_arr, axes):
        ax.imshow(img)
        ax.axis('off')
    plt.tight_layout()
    plt.show()


plotImages(sample_training_images[:2])

model = Sequential([
    Conv2D(16, 3, padding='same', activation='relu', input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
    MaxPooling2D(),
    Conv2D(32, 3, padding='same', activation='relu'),
    MaxPooling2D(),
    Conv2D(64, 3, padding='same', activation='relu'),
    MaxPooling2D(),
    Flatten(),
    Dense(512, activation='relu'),
    Dense(len(classes), activation='softmax')
])

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

history = model.fit_generator(
    train_data_gen,
    steps_per_epoch=total_train // batch_size,
    epochs=epochs,
    validation_data=val_data_gen,
    validation_steps=total_val // batch_size
)

plotImages(sample_test_images[:5])

STEP_SIZE_TEST = val_data_gen.n // val_data_gen.batch_size
val_data_gen.reset()
pred = model.predict_generator(val_data_gen,
                               steps=STEP_SIZE_TEST,
                               verbose=1)

predicted_class_indices = np.argmax(pred, axis=1)


labels = (train_data_gen.class_indices)
print(labels)
labels = dict((v,k) for k,v in labels.items())


predictions = [labels[k] for k in predicted_class_indices]

print(predictions)