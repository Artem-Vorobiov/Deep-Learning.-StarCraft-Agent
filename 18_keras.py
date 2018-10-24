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

noww         = datetime.datetime.strftime(datetime.datetime.now(), "%Y/%m/%d_%H:%M:%S")
pos_data_dir = 'train_data_2'
neg_data_dir = 'negative_data_2'
MODEL_NAME   = 'BasicCNN-10-epochs-0.0001-SECOND'
parent_root  = '/Users/tim/Documents/NN_MY'
parent_root  = '/Users/tim/Documents/NN_MY'
basic_path   = os.getcwd()


################################################################################
################################################################################
#								STEP 1

model = Sequential()

model.add(Conv2D(32, (3, 3), padding='same',
                 input_shape=(176, 200, 1),
                 activation='relu'))					#	Adjusting input.shape
model.add(Conv2D(32, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.2))

model.add(Conv2D(64, (3, 3), padding='same',
                 activation='relu'))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.2))

model.add(Conv2D(128, (3, 3), padding='same',
                 activation='relu'))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.2))

model.add(Flatten())
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(2, activation='softmax'))				# Somehow matches with labels = [0,1] 

learning_rate = 0.0001
opt = keras.optimizers.adam(lr=learning_rate, decay=1e-6)

model.compile(loss='categorical_crossentropy',
              optimizer=opt,
              metrics=['accuracy'])

tensorboard = TensorBoard(log_dir="/Users/tim/Documents/NN_MY/STAGE1")

# if os.path.exists('{}'.format(MODEL_NAME)):
#     model = keras.models.load_model("{}".format(MODEL_NAME))
#     print('model loaded!')
################################################################################
################################################################################








################################################################################
################################################################################
#								STEP 2						
def makeup_pos_train_data():
	pos_training_data = []
	count = 1
	for file in tqdm(os.listdir()):
		where1  = os.getcwd()
		loading = np.load(file)
		count  += 1
		pos_training_data.append([[loading],[1,0]])
		print(count)
	shuffle(pos_training_data)
	# np.save('{}/train_data_POS.npy'.format(parent_root), pos_training_data)
	return pos_training_data

def makeup_neg_train_data():
	neg_training_data = []
	count = 1
	for file in tqdm(os.listdir()):
		where1  = os.getcwd()
		loading = np.load(file)
		count  += 1
		neg_training_data.append([[loading],[0,1]])
	shuffle(neg_training_data)
	# np.save('{}/train_data_NEG.npy'.format(parent_root), neg_training_data)
	return neg_training_data
################################################################################
################################################################################








################################################################################
################################################################################
#								STEP 3
os.chdir(parent_root)

path1        = os.chdir('train_data_4')
pos_data = makeup_pos_train_data()
path2        = os.chdir('/Users/tim/Documents/NN_MY/negative_data_4')
current_path = os.getcwd()
neg_data = makeup_neg_train_data()

train = pos_data[:90]
test  = pos_data[-90:]

x_train = np.array([i[0][0][0][1] for i in train]).reshape(-1, 176, 200, 1)
y_train = np.array([i[1] for i in train])


##############################################################################################

# for i in train:
	# print('\n\n', i) 				# We are into level 2
	# print('\n\n', i[0]) 			# We are into level 3
	# print('\n\n', i[0][0]) 		# We are into level 4
	# print('\n\n', i[0][0][0])		# We are into level 5
	# print('\n\n', i[0][0][0][0])	# We are into level 6	[0. 0. 1. 0.]
	# print('\n\n', i[0][0][0][1])	# We are into level 6	[[0, 0, 0, ...,0, 0, 0], ... [ 0, 0, 0, ..., 0, 0, 0]]


##############################################################################################


x_test = np.array([i[0][0][0][1] for i in test]).reshape(-1, 176, 200, 1)
y_test = np.array([i[1] for i in test])

model.fit(x_train, y_train,
                  batch_size=64,
                  validation_data=(x_test, y_test),
                  shuffle=True,
                  epochs=10,
                  verbose=1, callbacks=[tensorboard])


os.chdir(parent_root)
model.save("BasicCNN-{}-epochs-{}-FIRST".format(10, learning_rate))
################################################################################
################################################################################







































#