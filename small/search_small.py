import pprint
import re
import operator

def count(terms):
	'''
		Input: List of words
		Output: Word counts
	'''
	counts = {}
	for term in terms:
		if term not in counts:
			counts[term] = 1
		else:
			counts[term] += 1 
	counts = sorted(counts.items(), key=operator.itemgetter(1))
	return counts

def parse(doc):
	'''
		Parse one document into a list of words
		 with only letters
	'''
	doc_input = open(doc)
	words = []
	regex = re.compile('[^a-zA-Z]')
	for i in doc_input.readlines():  # Split text to indiv. words
		temp_words = i.split()
		temp_words = [regex.sub('',w).lower() for w in temp_words]
		words.extend(temp_words)
	return words

def main():
	docs = ["doc1","doc2","doc3","doc4","doc5"]
	docs = ["./"+i for i in docs]
	terms = []  # List of documents; each doc is list of terms
	for i in docs:
		terms.append(parse(i))
	# pprint.pprint(terms)
	for t in terms: # Get word count for all docs
		pprint.pprint(count(t)[-5:])



main()