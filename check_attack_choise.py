import random 

def attack_choise():

	array_choise = [0,0,0,0]
	current_choise = random.randint(0,3)

	if current_choise == 0:
		array_choise[current_choise] = 1
		print('\n\t The choice is:\t Nothing')
		print('\n\t Array: {}'.format(array_choise))

	elif current_choise == 1:
	    array_choise[current_choise] = 1
	    print('\n\t The choice is:\t Attack known enemy units')
	    print('\n\t Array: {}'.format(array_choise))

	elif current_choise == 2:
	    array_choise[current_choise] = 1
	    print('\n\t The choice is:\t Attack Enemy Location')
	    print('\n\t Array: {}'.format(array_choise))

	elif current_choise == 3:
	    array_choise[current_choise] = 1
	    print('\n\t The choice is:\t Explore Map')
	    print('\n\t Array: {}'.format(array_choise))

attack_choise()