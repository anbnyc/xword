from __future__ import print_function
from lxml import html
from PIL import Image
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
		print('image retrieved')
		for chunk in img:
			file.write(chunk)
	print('image saved')

def parseAndPrintImage(url):
	imgLoc = './images/'+url[36:43]+'.png'
	im = Image.open(imgLoc)
	im = Image.composite(im, Image.new('RGB', im.size, 'white'), im)
	im.show()
	print('image loaded and cleaned')
	for i in range(15):
		row = list()
		for j in range(15):
			boxOuter = (j*30,i*30,j*30+30,i*30+30)
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

url = sys.argv[1] if len(sys.argv) > 1 else 'http://www.nytcrossword.com/2017/01/0102-17-new-york-times-crossword.html'
saveImage(url)
parseAndPrintImage(url)