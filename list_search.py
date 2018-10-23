
my_array = []

def fill_list(l, n):
    for i in range(1, n+1):
        l.append(i)
    return l

look = fill_list(my_array, 111)
print(look)
print('\n')
print(look[:-50]) 	# 	Итерирует до того момента пока не останется 50 НЕ проитерированых элементов
print('\n')
print(look[-50:])	# 	Итерирует через 50 последниъ элементов в массиве
print('\n')