from lxml import html
import requests
import calendar
import json

def zero(n):
	if len(str(n)) == 1:
		return "0"+str(n)
	else:
		return str(n)

def retrieve(url):
	try:
		page = requests.get(url)
		tree = html.fromstring(page.content)
		raw = [x for x in tree.xpath('//i/text()') if x != '\n']
		puzzle = list()
		direction = "Across"
		lastLocNum = 0
		for d in raw:
			dotPos = d.index(".")
			locNum = d[1:dotPos]
			if direction == "Across":
				if int(locNum) < lastLocNum:
					direction = "Down"
				else:
					lastLocNum = int(locNum)
			location = locNum+"-"+direction
			clue, answer = d[dotPos+1:].split(':')
			puzzle.append({
				"location": location,
				"clue": clue.strip(),
				"answer": answer.strip()
			})
		return puzzle
	except:
		print(url)
		errors.append(url)

collection = []
errors = []
year = "2016"
for i in range(1,13):
	day = calendar.monthrange(int(year),i)[1]
	for j in range(1,day+1):
		url = "http://www.nytcrossword.com/2016/"+zero(i)+"/"+zero(i)+zero(j)+"-16-new-york-times-crossword.html"
		collection.append({
			"date": year+"-"+zero(i)+'-'+zero(j),
			"puzzle": retrieve(url)
		})

url = 'http://www.nytcrossword.com/2017/01/0131-17-new-york-times-crossword_31.html'
retrieve(url)

errorfile = open('./errors.txt','w')
errorfile.write('\n'.join(errors))
errorfile.close()

datafile = open('./data.json','w')
datafile.write(json.dumps(collection,indent=1))
datafile.close()