import json
import urllib
import functools
import itertools
# import spacy
import numpy as np
import re
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords

# nlp = spacy.load('en')
def cosine(v1, v2):
	v1 = list(map(lambda x: float(x),v1))
	v2 = list(map(lambda x: float(x),v2))
	return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

"""
Uses Google Knowledge Graph Search API to return articles
	clue (str): clue to pass as API query
	length (int): word length to filter response
"""
def getKnowledgeGraphCandidates(clue,length):
	api_key = 'AIzaSyCz3EetlDMLlyU7LLWUH2n1U7mhUfqyxRk'
	service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
	params = {
			'query': clue,
			'limit': 10,
			'indent': True,
			'key': api_key,
	}
	url = service_url + '?' + urllib.parse.urlencode(params)
	candidates = set()
	response = json.loads(urllib.request.urlopen(url).read())
	for element in response['itemListElement']:
		try:
			article = re.split(", |\. |\s",element["result"]["detailedDescription"]["articleBody"])
			candidates.update(set(filter(lambda x: len(x) == length,article)))
		except:
			if element["result"].get("name"):
				print("no results: ",element["result"]["name"])
	return candidates

"""
Uses NLTK WordNet
	clue (str): one-word clue for which to find syno-,hypo-,hyper-nyms. 
	length (int): length of expected answer
"""
def getWordnetCandidates(clue,length):
	clue = re.sub('['+string.punctuation+']','',clue.lower())
	if clue is not wn.morphy(clue):
		## TODO reverse the morph transform
		morphedclue = wn.morphy(clue)
		morph = clue.replace(morphedclue,'')
		clue = morphedclue
		print("morph-",morph)
	synsets = wn.synsets(clue)
	names = functools.reduce(lambda x,y: x+y.lemma_names(),synsets,[])
	for syn in synsets:
		if syn.hyponyms():
			for hyposet in syn.hyponyms():
				names += [lemma.name() for lemma in hyposet.lemmas()]
		if syn.hypernyms():
			for hyperset in syn.hypernyms():
				names += [lemma.name() for lemma in hyperset.lemmas()]
	names = list({x for x in names if len(x) == length})
	return names

"""
Uses spaCy word vectors
	clue (list): tokenized list of words whose vectors to sum
	length (int): length of expected answer
	ret_count (int): number of candidates to return
"""
def getSpacyCandidates(clue,length,vocab,ret_count):
	vecs = [x.vector for x in clue]
	vecsum = functools.reduce(lambda x,y: np.add(x,y),vecs)
	vocab = [w for w in vocab if len(w.orth_) == length and w not in clue]
	vocab.sort(key=lambda w: cosine(w.vector, vecsum))
	return {w.orth_ for w in vocab[-1*ret_count:]}

"""
Takes NLTK vocabulary list and returns dict sorted by length
	maxlen (int): longest word we want to store
"""
def sortVocab(maxlen):
	sortedvocab = {}
	keys = []
	for i in [w for w in nlp.vocab if w.has_vector and w.orth_.islower() and len(w.orth_) <= maxlen]:
		k = len(i.orth_)
		if k not in keys:
			sortedvocab[k] = []
			keys.append(k)
		sortedvocab[k].append(i)
	return sortedvocab

"""
Takes array of clues and appends candidate answers
"""
def getCandidates(clues):
	vocab = sortVocab(15)
	for i,v in enumerate(clues[52:]):
		clue = v['clue']
		length = v['length']
		print(clue,length)
		if clue.find(' ') == -1:
			v["candidates_wordnet"] = getWordnetCandidates(clue,length)
			print('candidates_wordnet',v["candidates_wordnet"])
		elif "___" in clue:
			print(clue)
		else:
			clue_tokens = [nlp.vocab[x.lower_] for x in nlp(clue) if x.pos_ == "NOUN" or x.pos_ == "PROPN"]
			v["candidates_vec"] = getSpacyCandidates(clue_tokens,length,vocab[length],5)
			clue_tokens = [nlp.vocab[x] for x in clue.split() if x not in stopwords.words('english')]
			v["candidates_vec"].update(getSpacyCandidates(clue_tokens,length,vocab[length],5))
			print('candidates_vec', v["candidates_vec"])
			clue_tokens = getTokensForKGSearch(clue,True)
			v["candidates_know"] = set()
			if clue_tokens != '':
				v["candidates_know"].update(getKnowledgeGraphCandidates(clue_tokens,length))
			clue_tokens = getTokensForKGSearch(clue,False)
			if clue_tokens != '':
				v["candidates_know"].update(getKnowledgeGraphCandidates(clue_tokens,length))
			print('candidates_know:', v["candidates_know"])
		clues[i] = v
	return clues

"""
Tokenize clue return words with specific POS
	clue (str): clue to get pos_
	properonly (bool): include only proper nouns
"""
def getTokensForKGSearch(clue,properonly = True):
	clue = clue[:1].lower() + clue[1:]
	tokens = nltk.pos_tag(nltk.word_tokenize(clue))
	lookup = ["NNP","NNPS"] if properonly else ["NNP","NNPS","NN","NNS"]
	ret = " ".join([i for (i,j) in tokens if j in lookup])
	return ret

"""
Opens JSON file and passes clues to parse function
	fileloc (str): path to JSON file
"""
def loadPuzzle(fileloc):
	with open(fileloc,'r') as f:
		puzzle = json.loads(f.read())[0]
		puzzle['clues'] = getCandidates(puzzle['clues'])
		if input("print to file? y/n") == 'y':
			f.write(json.dumps(puzzle,indent=1))

loadPuzzle('./data/merge_0102-17.json')