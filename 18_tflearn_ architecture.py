import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
import tensorflow as tf
import cv2                 # working with, mainly resizing, images
import numpy as np         # dealing with arrays
import os                  # dealing with directories
from random import shuffle # mixing up or currently ordered data that might lead our network astray in training.
from tqdm import tqdm 	   # a nice pretty percentage bar for tasks. Thanks to viewer Daniel BA1/4hler for this suggestion
import datetime

noww = datetime.datetime.strftime(datetime.datetime.now(), "%Y/%m/%d_%H:%M:%S")

pos_data_dir = 'train_data'
neg_data_dir = 'negative_data'
MODEL_NAME   = 'dogsvscats-{}.model'.format(noww)
parent_root = '/Users/tim/Documents/NN_MY'


# path1 = os.listdir(train_dir)
parent_root = '/Users/tim/Documents/NN_MY'
basic_path  = os.getcwd()
print('\n\t\t\t\tBEGAN\n')

def makeup_pos_train_data():
	pos_training_data = []
	count = 1
	for file in tqdm(os.listdir()):
		where1 = os.getcwd()
		print('\n Im there {}'.format(where1))

		loading = np.load(file)

		print('\n Numpy {} - {}'.format(count,loading))
		print(type(loading))

		count += 1
		# print('\n {}. Loop through folder: {}'.format(count,file))

		pos_training_data.append([[loading],[1,0]])
	shuffle(pos_training_data)
	# np.save('{}/train_data_POS.npy'.format(parent_root), pos_training_data)
	return pos_training_data


def makeup_neg_train_data():
	neg_training_data = []
	count = 1
	for file in tqdm(os.listdir()):
		where1 = os.getcwd()
		print('\n Im there {}'.format(where1))

		loading = np.load(file)

		print('\n Numpy {} - {}'.format(count,loading))
		print(type(loading))

		count += 1
		neg_training_data.append([[loading],[0,1]])
	shuffle(neg_training_data)
	# np.save('{}/train_data_NEG.npy'.format(parent_root), neg_training_data)
	return neg_training_data



path1  = os.chdir('train_data')
pos_data = makeup_pos_train_data()
print('\n\n\t\t\t\tINTERMEDIATE STEP\n')

path2  = os.chdir('/Users/tim/Documents/NN_MY/negative_data')
current_path = os.getcwd()
print('\n ', current_path)
print('\n\n')


neg_data = makeup_neg_train_data()
print('\n\t\t\t\tENDS UP')


##############################################################################################
##############################################################################################

tf.reset_default_graph()

#               СТАНДАРТНАЯ АРХИТЕКТУРА НЕЙРОННОЙ СЕТИ
#                           НАЧАЛО

convnet = input_data(shape=[None, 176, 200, 1], name='input')

convnet = conv_2d(convnet, 32, 5, activation='relu')
convnet = max_pool_2d(convnet, 5)

convnet = conv_2d(convnet, 64, 5, activation='relu')
convnet = max_pool_2d(convnet, 5)

convnet = conv_2d(convnet, 128, 5, activation='relu')
convnet = max_pool_2d(convnet, 5)

convnet = conv_2d(convnet, 64, 5, activation='relu')
convnet = max_pool_2d(convnet, 5)

convnet = conv_2d(convnet, 32, 5, activation='relu')
convnet = max_pool_2d(convnet, 5)

convnet = fully_connected(convnet, 1024, activation='relu')
convnet = dropout(convnet, 0.8)

convnet = fully_connected(convnet, 2, activation='softmax')
convnet = regression(convnet, optimizer='adam', learning_rate=1e-3, loss='categorical_crossentropy', name='targets')

model = tflearn.DNN(convnet, tensorboard_dir='log')

##############################################################################################
##############################################################################################

if os.path.exists('{}.meta'.format(MODEL_NAME)):
    model.load(MODEL_NAME)
    print('model loaded!')

train = pos_data[:50]
test  = pos_data[-50:]

X = [i[0] for i in train]
Y = np.array([i[1] for i in train]).reshape(-1, 176, 200, 1)

test_x = [i[0] for i in test] 
test_y = np.array([i[1] for i in test]).reshape(-1, 176, 200, 1)

model.fit({'input': X}, {'targets': Y}, n_epoch=5, validation_set=({'input': test_x}, {'targets': test_y}), 
    snapshot_step=500, show_metric=True, run_id=MODEL_NAME)

model.save(MODEL_NAME)