#	Deleter

import os
from tqdm import tqdm 

path  = os.chdir('negative_data_2')
data  = os.listdir()

print(data)

for file in tqdm(data):
	if file == '.DS_Store':
		os.remove('.DS_Store')
		print('Removed')
	else:
		print('Nope ')