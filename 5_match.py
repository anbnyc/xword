
# def findMatches(puzzle):

import string

def getCoordsLookup(puzzle):
	clues = puzzle['clues']
	clues = concatCands(clues)
	grid = puzzle['grid']
	lookup = dict()
	for i,row in enumerate(grid):
		for j,cell in enumerate(row):
			if cell != "  ":
				entry = dict()
				relevant_clues = [x for x in clues if [i,j] in x['coords']]
				for clue in relevant_clues:
					position = clue['coords'].index([i,j])
					cands = [(x.lower()[position],x.lower()) for x in clue['cands'] if x.lower()[position] not in string.punctuation]
					for cand in cands:
						if not entry.get(cand[0]):
							entry[cand[0]] = {"Across":[],"Down":[]}
						entry[cand[0]][clue['location'].split("-")[1]].append(cand[1])
				lookup[str(i)+"_"+str(j)] = entry
	return lookup

def concatCands(clues):
	for index,clue in enumerate(clues):
		clue['cands'] = []
		for i in ['cand_vec','cand_kg','cand_wn']:
			if clue.get(i):
				clue['cands'] += clue[i]
		clues[index] = clue
	return clues

puzzle = json.load(open('./data/merge_0102-17_cands.json','r'))
print(json.dumps(getCoordsLookup(puzzle),indent=1))

#success = ['AWL','IRE','HAITIAN','IONS','TWIG','LYE','ABLE','LAWS','HOPE','HOLY','GENE','CICADAS','ATE','ENEMY','BOT','WOES','OBOE','ATOMS','ADS']
# tally = [[1, 0, 1], [1, 1, 1], [0, 1, 0], [1, 1, 1], [1, 0, 1], [0, 1, 1], [0, 1, 0], [1, 1, 1], [0, 1, 1], [1, 0, 0], [1, 0, 0], [0, 1, 1], [0, 1, 1], [1, 1, 1], [1, 0, 1], [1, 1, 1], [1, 1, 1], [1, 0, 0], [1, 1, 1]]
# tally = []
# for cl in clues:
# 	clue = cl['clue']
# 	length = cl['length']
# 	answer = cl['answer']
# 	if answer in success:
# 		formulations = []
# 		formulations.append([nlp.vocab[x.lower_] for x in nlp(clue) if x.pos_ == "NOUN" or x.pos_ == "PROPN"])
# 		formulations.append([nlp.vocab[x] for x in clue.split() if x not in stopwords.words('english')])
# 		formulations.append([nlp.vocab[x.lower_] for x in nlp(clue) if x.pos_ is not "PART"])
# 		score = [0,0,0]
# 		for i,clue_tokens in enumerate(formulations):
# 			if len(clue_tokens) != 0:
# 					cands = getSpacyCandidates(clue_tokens,length,vocab[length],5)
# 					if re.sub(" ","",answer.lower()) in [x.lower() for x in cands]:
# 						print(i,answer,cands)
# 						score[i] += 1
# 		tally.append(score)
# print(tally)