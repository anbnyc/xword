from __future__ import print_function
from lxml import html
from PIL import Image
from utils import *
import calendar
import pytesseract
import requests
import string
import sys

def saveImage(url):
	page = requests.get(url)
	tree = html.fromstring(page.content)
	path = '//a[@href="'+url+'"]/img/@src'
	imgUrl = tree.xpath(path)[0]
	with open('./images/'+url[36:43]+'.png','wb') as file:
		img = requests.get(imgUrl,stream=True)
		for chunk in img:
			file.write(chunk)

def parseAndPrintImage(url,nSquares):
	imgLoc = './images/'+url[36:43]+'.png'
	im = Image.open(imgLoc)
	im = Image.composite(im, Image.new('RGB', im.size, 'white'), im)
	pps = im.size[0]/nSquares
	# im.show()
	for i in range(nSquares):
		row = list()
		for j in range(nSquares):
			boxOuter = (j*pps,i*pps,j*pps+pps,i*pps+pps)
			tile = im.crop(boxOuter)
			# tile.save('./images/tile_'+str(i)+'_'+str(j)+'.jpg')
			if not tile.getbbox():
				tileText = " "
			else:
				boxInner = (7,9,27,27)
				tileInner = tile.crop(boxInner)
				tileText = pytesseract.image_to_string(tileInner,config="-psm 10 -l eng -c tessedit_char_whitelist="+string.ascii_uppercase)
				## this is hacky - find a better way
				tileText = "I" if tileText == "" else tileText
			row.append(tileText)
		print(" ".join(row))

def saveMultipleImages():
	year = "2017"
	for i in range(1,2):
		day = calendar.monthrange(int(year),i)[1]
		for j in range(1,day+1):
			url = "http://www.nytcrossword.com/"+year+"/"+zero(i)+"/"+zero(i)+zero(j)+"-"+year[2:]+"-new-york-times-crossword.html"
			saveImage(url)

# url = sys.argv[1] if len(sys.argv) > 1 else 'http://www.nytcrossword.com/2017/01/0102-17-new-york-times-crossword.html'
# saveImage(url)
# parseAndPrintImage(url,15)
saveMultipleImages()