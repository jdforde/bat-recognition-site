# TEST SAVED MODEL

import numpy as np
import tensorflow as tf
import keras as keras

# Main directory for model and IS_TEST.jpeg

# Must manually add class names
class_names = ['Bat', 'Not Bat']

################################################################################
# LOAD MODEL
model_directory = 'C:\\Users\\Jakob\\Documents\\Projects\\BatRecognitionEngine\\size_1K_epochs_200'
model = tf.keras.models.load_model(model_directory)

################################################################################
# LOAD AND PREPARE SINGULAR IMAGE
img_height = 180
img_width = 180

img = keras.preprocessing.image.load_img('C:\\Users\\Jakob\Pictures\\BatRecognition\\NotBat\\testclip_4.mp4_1.png', target_size=(img_height, img_width))
img_array = keras.preprocessing.image.img_to_array(img)
img_array = tf.expand_dims(img_array, 0)

################################################################################
# PREDICT AND OUTPUT RESULTS

predictions = model.predict(img_array)
score = tf.nn.softmax(predictions[0])
print(
    "This image most likely belongs to {} with a {:.2f} percent confidence.".format(class_names[np.argmax(score)], 100 * np.max(score))
)