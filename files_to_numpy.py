import numpy as np         # dealing with arrays
import os                  # dealing with directories
from random import shuffle # mixing up or currently ordered data that might lead our network astray in training.
from tqdm import tqdm 	   # a nice pretty percentage bar for tasks. Thanks to viewer Daniel BA1/4hler for this suggestion
import datetime

path_to_docs        = '/Users/tim/Documents/NN_MY/train_data_2'
path_to_parent_root = '/Users/tim/Documents/NN_MY'
os.getcwd()
os.chdir(path_to_docs)

def to_aggregate(path):
	pos_data = []
	collect_files = os.listdir(path)
	for file in collect_files:
		if file == '.DS_Store':
			collect_files.remove(file)
		else:
			extraction_numpy = np.load(file)
			pos_data.append(extraction_numpy)
			shuffle(pos_data)
			np.save('{}/pos_checking.npy'.format(path_to_parent_root), pos_data)
	print(pos_data)

to_aggregate(path_to_docs)