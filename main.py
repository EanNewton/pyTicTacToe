import random

grid = [['-' for x in range(3)] for x in range(3)]
counter = 0
flag = True
move = []
movePrev = []
player = ''
ai = input('Choose difficulty: \n 0 - 2 player \n 1 - easy \n 2 - medium \n 3 - hard\n')

corners = [[0, 0], [0, 2], [2, 0], [2, 2]]
edges = [[0, 1], [1, 0], [1, 2], [2, 1]]

def winCheck(player, move):
	if grid[0][move[1]] == player and grid[1][move[1]] == player and grid[2][move[1]] == player:
		return False
	if grid[move[0]][0] == player and grid[move[0]][1] == player and grid[move[0]][2] == player:
		return False
	if grid[0][0] == player and grid[1][1] == player and grid[2][2] == player:
		return False	
	if grid[0][2] == player and grid[1][1] == player and grid[2][0] == player:
		return False
	return True

def printGrid():
	for i in range(3):
		print (str(i)+' '+str(grid[i]))

def takeBack():
	try:
		grid[movePrev[-1][0]][movePrev[-1][1]] = '-'
		movePrev.pop()
	except IndexError:
		print("Grid is empty, cannot go back!")
		pass
		
def placeMove(player, move):
	try:
		move = list(map(int, move))
		if grid[move[0]][move[1]] != '-':
			return -1
		else:
			movePrev.append(move)
			grid[move[0]][move[1]] = player
			flag = winCheck(player, move)
			return flag
	except IndexError:
		print("Invalid entry.")
		pass

def getRandom(player):
	result = -1
	while result == -1:
		result = placeMove(player, [random.randint(0, 2) for _ in range(2)])
	return result	
	
def blockWin(player):
	result = True
	taken = 0
	for i in range(3):
		for n in range(3):
			move = [i, n]
			taken = placeMove('X', move)
			result = winCheck('X', move)
			if taken != -1:
				takeBack()
			if result == False:
				result = placeMove(player, move)
				return result
	result = -1
	return result

def takeWin(player):
	result = True
	taken = 0
	for i in range(3):
		for n in range(3):
			move = [i, n]
			taken = placeMove(player, move)
			result = winCheck(player, move)
			if taken != -1:
				takeBack()
			if result == False:
				result = placeMove(player, move)
				return result
	result = -1
	return result

def expert(player):
	if len(movePrev) == 1:
		if movePrev[0] == [1, 1]:
			result = placeMove(player, random.choice(corners))
		else:
			result = placeMove(player, [1, 1])
	else:
		result = takeWin(player)
		if result == -1:
			result = blockWin(player)
	return result		

def dispatch_ai(operator, player):
	return {
		'1': lambda: getRandom(player),
		'2': lambda: blockWin(player),
		'3': lambda: expert(player),
	}.get(operator, lambda: None)()

while flag:
	if counter == 9:
		flag = False
		print("Stalemate!")
		break
			
	player = 'X' if counter % 2 == 0 else 'O'
	
	if int(ai) > 0 and player == 'O':
		flag = dispatch_ai(ai, player)
		if flag == -1:
			flag = dispatch_ai('1', player)
		if not flag:
			print(player+" wins!")
		counter += 1
	else:
		printGrid()
		flag = -1
		while flag == -1:	
			move = input(player+": ").split()
			if move[0] == 'back':
				for _ in range(2):
					takeBack()
				if counter > 0:
					counter -= 2
				printGrid()
			else:
				flag = placeMove(player, move)
				if not flag: 
					print(player+" wins!")
		counter += 1

printGrid()
