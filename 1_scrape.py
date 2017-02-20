from lxml import html
from utils import *
import requests
import calendar
import json
import string
import re

def retrieve(url):
	page = requests.get(url)
	tree = html.fromstring(page.content)
	raw = [x for x in tree.xpath('//i/text()') if x != '\n']
	clues = {
		"Across": list(),
		"Down": list()
	}
	direction = "Across"
	lastLocNum = 0
	for d in raw:
		try:
			dotPos = d.index(".")
			locNum = d[1:dotPos]
			if direction == "Across":
				if int(locNum) < lastLocNum:
					direction = "Down"
				else:
					lastLocNum = int(locNum)
			location = locNum+"-"+direction
			clue, answer = re.split('\s\:\s+(?=[A-Z\‘\-\.\…]+)',d[dotPos+1:])
			clues[direction].append({
				"location": location,
				"clue": clue.strip('[ \-\.]'),
				"answer": re.sub('['+string.punctuation+']','',answer)
			})
		except:
			try:
				clue, answer = re.split('\s+(?=[A-Z]{2,})',d[dotPos+1:],1)
				clues[direction].append({
					"location": location,
					"clue": clue.strip('[ \-\.]'),
					"answer": re.sub('['+string.punctuation+']','',answer)
				})
			except:
				print((url, d))
				errors.append((url, d))
	return clues

collection = []
errors = list()

def main():
	year = "2017"
	for i in range(1,2):
		day = calendar.monthrange(int(year),i)[1]
		for j in range(1,day+1):
			url = "http://www.nytcrossword.com/"+year+"/"+zero(i)+"/"+zero(i)+zero(j)+"-"+year[2:]+"-new-york-times-crossword.html"
			collection.append({
				"date": year+"-"+zero(i)+'-'+zero(j),
				"clues": retrieve(url)
			})

	errorfile = open('./errors.txt','w')
	errorfile.write('\n'.join(map(lambda x: x[0]+";"+x[1],errors)))
	errorfile.close()

	datafile = open('./data/data_'+year+'.json','w')
	datafile.write(json.dumps(collection,indent=1))
	datafile.close()

if __name__ == "__main__":
    main()