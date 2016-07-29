import sys

# Open files
gridpath = sys.argv[1]
dictpath = sys.argv[2]

DICT_FILE = open(dictpath, 'r')

# Storing the dictionary as a set to provide us with
# average case constant time membership checks
DICT = set() 

alphabetLen = 26

maxWordLen = [0 for i in xrange(alphabetLen)]
# maxWordLen[i] -> length of the longest word in the dictionary that begins with 
#					ord('A') + i

for line in DICT_FILE:
	DICT.add(line[:len(line)-1]) # Exclude terminating newline character

	firstChar = line[0]
	index = ord(line[0]) - ord('A')

	if(len(line)-1 > maxWordLen[index]):
		maxWordLen[index] = len(line)-1
		# Set maximum lengths

# wordSet contains all the words (but removes duplicates)
wordSet = set()

# sortedList contains all the words from wordSet but in 
# alphabetical order. We use this for our output
sortedList = []

class hexagonalGrid:

	GRID = None

	# GRID[l][i] will represent the node in the ith position of layer l
	# (when l is traversed clockwise from the top).

	def __init__(self, gridpath):
		GRID_FILE = open(gridpath, 'r')

		# Parsing grid file (honeycomb.txt)
		layersList = list(GRID_FILE )# List of strings
		numLayers = int(layersList[0])

		self.GRID = [None for i in xrange(numLayers)]

		# The honeycomb will be represented by a list of lists.
		for i in xrange(0,numLayers):
			self.GRID[i] = list(layersList[i+1])
			self.GRID[i].pop() # remove the newline character
			# GRID[i] -> letters (clockwise) in the ith layer		


	# Return the number of layers in the grid.
	def numLayers(self):
		return len(self.GRID)

	# Function that returns the neighbors of 
	# the node at position i in layer l

	# The formula used in this function are explained
	# in the README.

	def getNeighbors(self, l, i):

		neighborList = []

		if(l == 0):
			# the neighbors of the center of the grid are 
			# simply all the elements of layer 1
			return [(1,0),(1,1),(1,2),(1,3),(1,4),(1,5)]

		layerLen = 6*l

		# Get the two trivial neighbors that are in the same layer l.

		# Anti-CW neighbor
		neighborList.append((l,(i-1+layerLen)%layerLen))

		#CW neighbor
		neighborList.append((l,(i+1)%layerLen))

		# Get the neighbors in layer l-1
		group = i/l
		previousLayerLen = 6*(l-1)
		if(i % l == 0): # corner code
			neighborList.append((l-1, group*(l-1)))

		else:
			neighborList.append((l-1, i-group-1))
			neighborList.append((l-1, (i-group)%previousLayerLen))

		# Get the neighbors in layer l+1
		if(l == self.numLayers()-1):
			return neighborList

		if(i % l == 0):
			# 3 neighbors
			neighborList.append((l+1, (i-1+layerLen) % layerLen + group))
			neighborList.append((l+1, (i+layerLen) % layerLen + group))
			neighborList.append((l+1, (i+1 + layerLen) % layerLen + group))

		else:
			neighborList.append((l+1, group*(l+1) + i%l))
			neighborList.append((l+1, group*(l+1) + (i+1)%l))

		return neighborList


# This function first creates a hexagonal grid and a 
# visited grid with an identical structure. 

# We then use the principle that every node in the grid
# could be a possible starting letter for a word.
# Iterate over all letters in the board and every iteration 
# has a call to the function 'dfs' which does
# the bulk of the work (the depth first search).

def search():

	# instance of the class
	G = hexagonalGrid(gridpath)

	# visited grid keeps track of the nodes we've already visited
	visited = [None for i in xrange(G.numLayers())]
	for i in xrange(G.numLayers()):
		layer = G.GRID[i]
		visited[i] = [0 for j in xrange(len(layer))]

	# visited[i][j] = 1 if the node at layer i and position j has been visited

	for l in xrange(G.numLayers()):
		layer = G.GRID[l]
		for i in xrange(len(layer)):
			dfs(l, i, visited, "", G, maxWordLen[ord(G.GRID[l][i]) - ord('A')])

	# Put every element in the list
	for key in wordSet:
		sortedList.append(key)

	sortedList.sort()

	for word in sortedList:
		sys.stdout.write(word+"\n")


# This is the function that does the backtracking. 
# It's explained in the README but the general idea is
# that I use each node as a starting point and recursively contruct
# the current string until we have no new
# neighbors to visit or we've exceeded
# the maximum length of the longest word in the 
# dictionary starting with the first
# letter of the string.

def dfs(l, i, visited, str, G, maxLen):
	if(visited[l][i] == 1):
		# Cannot visit this again.
		return 
	elif(len(str) > maxLen):
		visited[l][i] = 0
		return 

	# Visit this node
	visited[l][i] = 1
	if((str + G.GRID[l][i]) in DICT):
		wordSet.add(str+G.GRID[l][i])

	# Recurse over every neighbor
	N = G.getNeighbors(l,i)
	for (m,n) in N:
		dfs(m,n,visited,str + G.GRID[l][i],G, maxLen)

	visited[l][i] = 0 # back track

if __name__ == "__main__":
	search()