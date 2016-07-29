This zipped file contains my implementation Quantcast.py.

It can be run as described in the handout:

python Quantcast.py path_to_honeycomb.txt path_to_dict.txt

The goal of this exercise was to find all the possible words from a dictionary that existed in 
a hexagonal grid of letters.

The method I used was to DFS starting at every letter(node) in the hexagonal grid.

Describing the structure of my grid:

I store the grid as a list of lists. 

GRID[m][n] would give us the node in layer m, clockwise position n. 
Note that the clockwise traversal starts from the top of the layer. 


DFS EXPLANATION:

The DFS is relatively straightforward. We visit a node, check if the concatenation with our
current string forms a word in the dictionary. If it does we add it to our wordSet. I will
come to why I use a set shortly. 

After adding the word to our set, we compute the neighbors of the node and recurse
to visit them. Note that I check whether a neighbor has been visited or not only after I 
recursively call dfs. I could check this before I call the function to prevent the wastage of 
stack frames but that's a minor optimization.

NEIGHBORS FUNCTION:

The difficult part of this was to find the formulas for the neighbors.

I distinguished the nodes of a hexagonal grid into two categories - Corner nodes and Middle nodes.

Every node obviously has two neighbors in its own layer.

However corner nodes have 3 neighbors in their outer layer and 1 in their inner while middle nodes
have 2 each. 

I used some manipulation to come up with the formulae after writing down quite a few examples and
trying to figure out a pattern. 

OPTIMIZATIONS:

A depth first search in such a hexagonal grid is going to be quite slow. We visit each node an exponential
number of times (I think it's factorial if I'm not wrong) and also have two loops over every node in the board giving
us a time complexity of O(N*N!) where N is the number of nodes in the hexagonal grid.

One optimization I came up with is keeping track of the longest word starting with every character in the alphabet.

For example, if the longest word beginning with X in the dictionary is XYLOPHONE, then I only recurse in my dfs at 
most 9 times when my word begins with X. This does change the complexity by a little and makes it dependent on the 
longest word length in the dictionary.

OUTPUT:

The output had to have unique words, lexicographically sorted. To remove duplicates, every time I find a word I add
it to the set. A set in Python does membership checks in constant time, so it will add a word to itself quickly and
efficiently. Now that we've rid ourselves of duplicates, we can simply sort the list in the typical sort time of O(Nlg N)
which will give us our answer.


THINGS TO THINK ABOUT:

This solution can definitely be made better. One idea I have (as a starting point only of course) is 
actually going from dictionary -> grid rather than grid -> dictionary. We look at the first letter
of a word in the dicionary, find it in the grid and check if any of the neighbors match the second character of the word.

Repeat this until we have exhausted the length of the word OR no neighbor matches the next letter of the word.

I feel this would be much more efficient, but I didn't have the time to code this up.

Appreciate your time taking a look at this, and thanks a lot for a wonderful exercise!