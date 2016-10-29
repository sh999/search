import pprint as pp
import re
import operator

def count_all(doc_counts):
	'''
		Input: Word counts for each doc
		Return: Word counts in corpus
			e.g. 'the' appears in corpus x times
	'''
	counts = {}
	for doc in doc_counts:
		for term in doc:  # Go through each term in each doc, increment word count each time
			if term[0] not in counts:
				counts[term[0]] = term[1]
			else:
				counts[term[0]] += term[1]
	counts = sorted(counts.items(), key=operator.itemgetter(1))
	return counts

def count_doc(terms):
	'''
		Input: List of words
		Return: Word counts
			e.g. 'the' appears in this doc, x times
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
	doc_terms = []  # List of documents; each doc is list of terms
	doc_term_counts = []
	for d in docs: # Build list of terms for each doc
		doc_terms.append(parse(d))
	for t in doc_terms: # Get word count for all docs
		doc_term_counts.append(count_doc(t))
	corpus_counts = count_all(doc_term_counts)
	# pp.pprint(corpus_counts)
	pp.pprint(doc_term_counts[0])

main()