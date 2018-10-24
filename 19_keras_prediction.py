import keras  # Keras 2.1.2 and TF-GPU 1.9.0
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.callbacks import TensorBoard
# import random
import cv2                 # working with, mainly resizing, images
import numpy as np         # dealing with arrays
import os                  # dealing with directories
from random import shuffle # mixing up or currently ordered data that might lead our network astray in training.
from tqdm import tqdm 	   # a nice pretty percentage bar for tasks. Thanks to viewer Daniel BA1/4hler for this suggestion
import datetime

MODEL_NAME   = 'BasicCNN-10-epochs-0.0001-FIRST'

if os.path.exists('{}'.format(MODEL_NAME)):
    model = keras.models.load_model("{}".format(MODEL_NAME))
    print('model loaded!')

test_data = np.load('pos_checking.npy')

# print('\n\n TEST DATA:', test_data[0][0][1])
# for i in test_data:
# 	print('\n\n\n', i[0][1])

input_test_data = np.array([i[0][1] for i in test_data]).reshape(-1, 176, 200, 1)
# print('\n\n', input_test_data[0].shape)
# print('\n\n TYPE:',      type(test_data))		#	<class 'numpy.ndarray'>
# print('\n\n SHAPE:',     test_data.shape)		#	(29,)

# print('\n\n TYPE:',      type(test_data[0]))	#	<class 'numpy.ndarray'>
# print('\n\n SHAPE:',     test_data[0].shape)	#	(190, 2)

# print('\n\n TYPE:',      type(test_data[0][0]))	#	<class 'numpy.ndarray'>
# print('\n\n SHAPE:',     test_data[0][0].shape)

# data      = test_data.reshape(176, 200, 1)
model_out = model.predict([input_test_data])

print(model_out)