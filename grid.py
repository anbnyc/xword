from PIL import Image
import sys
import json

nSquares = 15

def zero(n):
	if len(str(n)) == 1:
		return "0"+str(n)
	else:
		return str(n)

class Clue(object):
	def __init__(self,direction,locNum,coords=(0,0),length=0):
		self.location = str(locNum)+"-"+direction,
		self.coords = coords,
		self.length = length
	def __str__(self):
		return str(self)

class crossword(object):
	def __init__(self,grid,clues):
		self.grid = grid,
		self.clues = clues

def getBlackSquares(imgLoc):
	im = Image.open(imgLoc)
	im = Image.composite(im, Image.new('RGB', im.size, 'white'), im)
	pps = im.size[0]/nSquares
	return [(i,j) for i in range(15) for j in range(15) if not im.crop((j*pps,i*pps,j*pps+pps,i*pps+pps)).getbbox()]

def placeClues(blackSquares):
	print(blackSquares)
	blank = "  "
	n = 1
	grid = list()
	## TODO change to a list - doesn't need to be separated by direction
	clues = {
		"Across": list(),
		"Down": list()
	}
	for i in range(nSquares):
		grid.append(list())
		for j in range(nSquares):
			if len(blackSquares) > 0 and (i,j) == blackSquares[0]:
				grid[i].append(blank)
				blackSquares.pop(0)
			else:
				if i == 0 and j == 0:
					grid[i].append(zero(n))
					clues["Down"].append(Clue("Down",n,(i,j)))
					clues["Across"].append(Clue("Across",n,(i,j)))
					n+=1
				elif i == 0:
					grid[i].append(zero(n))
					clues["Down"].append(Clue("Down",n,(i,j)))
					n+=1
				elif j == 0:
					grid[i].append(zero(n))
					clues["Across"].append(Clue("Across",n,(i,j)))
					n+=1
				elif grid[i][j-1] == blank and grid[i-1][j] == blank:
					grid[i].append(zero(n))
					clues["Across"].append(Clue("Across",n,(i,j)))
					clues["Down"].append(Clue("Down",n,(i,j)))
					n+=1
				elif grid[i][j-1] == blank:
					grid[i].append(zero(n))
					clues["Across"].append(Clue("Across",n,(i,j)))
					n+=1
				elif grid[i-1][j] == blank:
					grid[i].append(zero(n))
					clues["Down"].append(Clue("Down",n,(i,j)))
					n+=1
				else:
					grid[i].append("__")
		print(" ".join(grid[i]))
	# print('\n')
	return grid

url = sys.argv[1] if len(sys.argv) > 1 else 'http://www.nytcrossword.com/2017/01/0102-17-new-york-times-crossword.html'
placeClues(getBlackSquares('./images/'+url[36:43]+'.png'))