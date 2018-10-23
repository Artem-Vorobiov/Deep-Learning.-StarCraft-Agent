#	How namy files inside folder

import os
import datetime

listFandF = os.listdir()							#	Массив со всеми файлами и папками указанной директории
print('\n Содержимое папки /NN_MY', listFandF)		#	['how_many_files_in_folder.py', ...  '1_NN_start_off.py']
print('\n Тип переменной', type(listFandF))			#	<class 'list'>

train1 = os.getcwd()								#	Отдает строку в виде Путя где мы сейчас находимся
print('\n Отдает путь где сейчас программа', train1)#	/Users/tim/Documents/NN_MY
print('\n Тип переменной', type(train1))			#	<class 'str'>

train2 =os.chdir('train_data')						#	Переходит из нынешнего места по указанному пути
print('\n Происходит смена пути', train2)			#	None
print('\n Тип переменной', type(train2))			#	<class 'NoneType'>

train3 = os.getcwd()								#	Отдает строку в виде Путя где мы сейчас находимся
print('\n Отдает путь где сейчас программа', train3)#	/Users/tim/Documents/NN_MY/train_data
print('\n Тип переменной', type(train3))			#	<class 'str'>


step2 = os.listdir()
print('\n Содержимое папки train_data', step2)		#	['1540068160.npy', ...  '1540062051.npy']
print('\n Тип переменной', type(step2))				#	<class 'list'>

count = 0 
for i in step2:
	count += 1

print('\n\t Количесиво файлов в папке - ', count)


now = datetime.datetime.now()
os.chdir('../')
step3 = os.getcwd()

with open('amount.txt', 'a') as f:
	f.write('Data {} - It is {} files inside {}'.format(now, count, step3))