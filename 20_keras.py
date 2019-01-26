import keras  # Keras 2.1.2 and TF-GPU 1.9.0
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.callbacks import TensorBoard
# import random
import cv2                 # working with, mainly resizing, images
import numpy as np         # dealing with arrays
import os                  # dealing with directories
import random
from tqdm import tqdm 	   # a nice pretty percentage bar for tasks. Thanks to viewer Daniel BA1/4hler for this suggestion
import datetime

noww         = datetime.datetime.strftime(datetime.datetime.now(), "%Y/%m/%d_%H:%M:%S")
pos_data_dir = 'last_easy_pos'
neg_data_dir = 'last_easy_neg'
MODEL_NAME   = 'BasicCNN-5000-epochs-0.001-FULL'
parent_root  = '/Users/tim/Documents/NN_MY'
basic_path   = os.getcwd()


################################################################################
################################################################################
################################################################################
################################################################################
#								Just Trained Positive


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
model.add(Dense(4, activation='softmax'))				# Somehow matches with labels = [0,1] 

learning_rate = 0.0001
opt = keras.optimizers.adam(lr=learning_rate, decay=1e-6)

model.compile(loss='categorical_crossentropy',
              optimizer=opt,
              metrics=['accuracy'])

tensorboard = TensorBoard(log_dir="/Users/tim/Documents/NN_MY/STAGE3")


# if os.path.exists('{}'.format(MODEL_NAME)):
#     model = keras.models.load_model("{}".format(MODEL_NAME))
#     print('model loaded!')

def data_length():
	choices = {"no_attacks": no_attacks,
				"attack_enemy_units": attack_enemy_units,
				"attack_enemy_start": attack_enemy_start,
				"explore": explore}
	total_data = 0
	lengths = []
	for choice in choices:
		# print("Length of {} is: {}".format(choice, len(choices[choice])))
		total_data += len(choices[choice])
		lengths.append(len(choices[choice]))

	return lengths, total_data


train_data_dir = "last_easy_pos"
count = 0 

hm_epochs = 10

for i in range(hm_epochs):
	print("\n Currnet Epoch = {} ", i)

	current     = 0
	increment   = 4
	not_maximum = True

	all_files = os.listdir(train_data_dir)
	random.shuffle(all_files)
	maximum = len(all_files)

	while not_maximum:
		print("WORKING ON {}:{}".format(current, current+increment))
		no_attacks		   = []
		attack_enemy_units = []
		attack_enemy_start = []
		explore 		   = []

		for file in all_files[current:current+increment]:
			full_path = os.path.join(train_data_dir, file)
			data = np.load(full_path)
			data = list(data)			#	Дает доступ к данным и возмодность итерировать среди них

			for d in data:
				choice = np.argmax(d[0])
				if choice == 0:
					no_attacks.append([d[0], d[1]])
				elif choice == 1:
					attack_enemy_units.append([d[0], d[1]])
				elif choice == 2:
					attack_enemy_start.append([d[0], d[1]])
				elif choice == 3:
					explore.append([d[0], d[1]])

		lengths, total_data = data_length()
		print('Lenghts: {}, Total_data: {}'.format(lengths, total_data))
		lowest_data = min(lengths)

		no_attacks 		   = no_attacks[:lowest_data]
		attack_enemy_units = attack_enemy_units[:lowest_data]
		attack_enemy_start = attack_enemy_start[:lowest_data]
		explore 		   = explore[:lowest_data]

		random.shuffle(no_attacks)
		random.shuffle(attack_enemy_units)
		random.shuffle(attack_enemy_start)
		random.shuffle(explore)

		train_data = no_attacks + attack_enemy_units + attack_enemy_start + explore
		random.shuffle(train_data)
		print(len(train_data))

		test_size = 100
		batch_size = 128
		print(len(train_data))

		x_train = np.array([i[1] for i in train_data[:-test_size]]).reshape(-1, 176, 200, 1)
		y_train = np.array([i[0] for i in train_data[:-test_size]])

		x_test = np.array([i[1] for i in train_data[-test_size:]]).reshape(-1, 176, 200, 1)
		y_test = np.array([i[0] for i in train_data[-test_size:]])

		# print('\n\n X TRAIN', x_train)  #    [[[[0 0 0], ..., [0 0 0]]]] - map
		# print('\n\n Y TEST', y_test)    #    [[1. 0. 0. 0.], ... , [0. 0. 0. 1.]]
		# xxx = np.array([i[1] for i in train_data[:-test_size]]).shape
		# print(xxx)

		model.fit(x_train, y_train,
			batch_size=batch_size,
			validation_data=(x_test, y_test),
			shuffle=True,
			epochs=1,
			verbose=1, callbacks=[tensorboard])

		model.save("BasicCNN-5000-epochs-0.001-Last")
		print('\n\n\t After saving, ALL: {}'.format(all_files))
		print('\n\n\t After saving, current: {}'.format(current))
		print('\n\n\t After saving, current+increment: {}'.format(current+increment))
		current += increment
		if current >= maximum:
			not_maximum = False
			print('\n\n\nFALSE')




# x_train = np.array([i[0][0][0][1] for i in train]).reshape(-1, 176, 200, 1)
# y_train = np.array([i[1] for i in train])
##############################################################################################

# for i in train:
	# print('\n\n', i) 				# We are into level 2
	# print('\n\n', i[0]) 			# We are into level 3
	# print('\n\n', i[0][0]) 		# We are into level 4
	# print('\n\n', i[0][0][0])		# We are into level 5
	# print('\n\n', i[0][0][0][0])	# We are into level 6	[0. 0. 1. 0.]
	# print('\n\n', i[0][0][0][1])	# We are into level 6	[[0, 0, 0, ...,0, 0, 0], ... [ 0, 0, 0, ..., 0, 0, 0]]


##############################################################################################
# x_test = np.array([i[0][0][0][1] for i in test]).reshape(-1, 176, 200, 1)
# y_test = np.array([i[1] for i in test])

# model.fit(x_train, y_train,
#                   batch_size=64,
#                   validation_data=(x_test, y_test),
#                   shuffle=True,
#                   epochs=10,
#                   verbose=1, callbacks=[tensorboard])


# os.chdir(parent_root)
# model.save("BasicCNN-{}-epochs-{}-FIRST".format(10, learning_rate))
################################################################################
################################################################################







































#