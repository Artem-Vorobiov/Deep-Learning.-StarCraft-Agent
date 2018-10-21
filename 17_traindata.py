import cv2                 # working with, mainly resizing, images
import numpy as np         # dealing with arrays
import os                  # dealing with directories
from random import shuffle # mixing up or currently ordered data that might lead our network astray in training.
from tqdm import tqdm 	   # a nice pretty percentage bar for tasks. Thanks to viewer Daniel BA1/4hler for this suggestion

pos_data_dir = 'train_data'
neg_data_dir = 'negative_data'
MODEL_NAME   = 'dogsvscats-{}.model'.format('2conv-basic')

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

		# print('\n Numpy {} - {}'.format(count,loading))
		print(type(loading))

		count += 1
		neg_training_data.append([[loading],[0,1]])
	shuffle(neg_training_data)
	# np.save('{}/train_data_NEG.npy'.format(parent_root), neg_training_data)
	return neg_training_data



path1  = os.chdir('train_data')
# pos_data = makeup_pos_train_data()
print('\n\n\t\t\t\tINTERMEDIATE STEP\n')

path2  = os.chdir('/Users/tim/Documents/NN_MY/negative_data')
current_path = os.getcwd()
print('\n ', current_path)
print('\n\n')


neg_data = makeup_neg_train_data()
print('\n\t\t\t\tENDS UP')


el = np.array([i[0] for i in neg_data])
ch_el = el.reshape(-1,176,200,1)
# print('\n {}'.format(ch_el))
print('\n {}'.format(ch_el.shape))
# print(neg_data)
# print('\n Type: ', type(neg_data))
# print('\n Second Element: {}'.format(el))