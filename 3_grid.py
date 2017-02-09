from PIL import Image
from utils import *
import sys
import json
import calendar

class Clue(object):
	def __init__(self,direction,locNum,coords=(0,0),length=0):
		self.location = str(locNum)+"-"+direction
		self.coords = coords
		self.length = length
		self.answer = ""
	def __repr__(self):
		return str({'location': self.location, 'coords': self.coords, 'length': self.length})

def getBlackSquares(imgLoc,nSquares):
	im = Image.open(imgLoc)
	im = Image.composite(im, Image.new('RGB', im.size, 'white'), im)
	pps = im.size[0]/nSquares
	return [(i,j) for i in range(nSquares) for j in range(nSquares) if not im.crop((j*pps,i*pps,j*pps+pps,i*pps+pps)).getbbox()]

def getNewClueWithLength(i,j,n,blackSquares,direction,nSquares):
	if direction == "Across":
		nextBlack = [q for (p,q) in blackSquares if i == p]
		len = (nextBlack[0] if nextBlack else nSquares) - j
	elif direction == "Down":
		nextBlack = [p for (p,q) in blackSquares if j == q]
		len = (nextBlack[0] if nextBlack else nSquares) - i
	return Clue(direction,n,(i,j),len)

def placeClues(blackSquares,nSquares):
	black = "  "
	n = 1
	grid = list()
	clues = {
		"Across": list(),
		"Down": list()
	}
	for i in range(nSquares):
		grid.append(list())
		for j in range(nSquares):
			if len(blackSquares) > 0 and blackSquares[0] == (i,j):
				grid[i].append(black)
				blackSquares.pop(0)
			else:
				if i == 0:
					if j == 0 or grid[i][j-1] == black:
						clues["Across"].append(getNewClueWithLength(i,j,n,blackSquares,"Across",nSquares))
					grid[i].append(zero(n))
					clues["Down"].append(getNewClueWithLength(i,j,n,blackSquares,"Down",nSquares))
					n+=1
				elif j == 0:
					if grid[i-1][j] == black:
						clues["Down"].append(getNewClueWithLength(i,j,n,blackSquares,"Down",nSquares))
					grid[i].append(zero(n))
					clues["Across"].append(getNewClueWithLength(i,j,n,blackSquares,"Across",nSquares))						
					n+=1
				elif grid[i][j-1] == black:
					grid[i].append(zero(n))
					clues["Across"].append(getNewClueWithLength(i,j,n,blackSquares,"Across",nSquares))
					n+=1
				elif grid[i-1][j] == black:
					grid[i].append(zero(n))
					clues["Down"].append(getNewClueWithLength(i,j,n,blackSquares,"Down",nSquares))
					n+=1
				else:
					grid[i].append("__")
		# print(" ".join(grid[i]))
	return clues, grid

def mergeWithClues():
	year = "2017"
	iyear = int(year)
	with open('./data/data_'+year+'.json','r') as f:
		clues_from_text = f.read()
		clues_from_text = json.loads(clues_from_text)
	data = list()
	for i in range(1,2):
		day = calendar.monthrange(int(year),i)[1]
		for j in [x for x in range(1,day) if x != 19 and x != 24]:
			nSquares = 21 if calendar.weekday(iyear, i, j) == 6 else 15
			url_date = zero(i)+zero(j)+"-"+year[2:]
			cal_date = year+"-"+zero(i)+'-'+zero(j)
			print(url_date,cal_date)
			date_clues_from_image, grid = placeClues(getBlackSquares('./images/'+url_date+'.png',nSquares),nSquares)
			date_clues_from_text = [x for x in clues_from_text if x["date"] == cal_date][0]['puzzle']
			merge = list()
			for dir in ("Across","Down"):
				merge += [{'location': a['location'], 'clue': a['clue'], 'coords': b.coords, 'length': b.length} for a in date_clues_from_text[dir] for b in date_clues_from_image[dir] if a['location'] == b.location]
			data.append({"date": cal_date, "clues": merge, "grid": grid})
	with open('./data/merge_'+year+'.json','w') as f:
		f.write(json.dumps(data,indent=1))

mergeWithClues()
