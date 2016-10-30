from __future__ import division
import pprint as pp
import re
import operator

def get_tfidfs(tfs, idfs):
	'''
		Input:
			tf: Word count for each doc
			idf: Inverse doc freq of each term in corpus
		Return:
			Each term in each doc will have a value (tf/idf for the term)
			So each doc will have a vector of the term values  
	'''
	# print "tf:"
	# pp.pprint(tfs)
	# print "idfs:"
	# pp.pprint(idfs)
	tfidfs = {}
	for doc_name in tfs:
		temp_doc = {}
		for term in tfs[doc_name]:
			# print term
			temp_tf = tfs[doc_name][term]
			temp_idf = idfs[term]
			temp_tfidf = temp_tf/temp_idf
			temp_doc[term] = (temp_tf,temp_idf,temp_tfidf)
			# tfidfs.append(([term[0],idfs[term[0]],term[1]/idfs[term[0]]]))
		tfidfs[doc_name] = temp_doc
	# print "tfidfs:"
	# pp.pprint(tfidfs)
	return tfidfs

def get_idfs(tfs):
	'''
		Input: Word counts for each doc 
		Return: Inverse doc freq (idf) for all terms
			idf for a term relates to how many docs have that term
	'''
	unique_terms = [] # All unique terms in corpus; used to check if a term is already seen 
	idfs = {}
	for doc_name in tfs:
		for term in tfs[doc_name]:
			if term not in unique_terms:
				# unique_terms.append(term[0])
				# idfs[term[0]] = 1
				unique_terms.append(term)
				idfs[term] = 1
			else:
				# idfs[term[0]] += 1
				idfs[term] += 1
	# idfs = sorted(idfs.items(), key=operator.itemgetter(1))
	return idfs

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

def get_tfs(doc_terms):
	'''
		Input: List of words
		Return: Word counts
			e.g. 'the' appears in this doc, x times
			{'doc1':{'the':10,'falls':3'...}, 'doc2':..., ...}
	'''
	all_counts = {}
	for doc_name in doc_terms:
		counts = {}
		all_counts[doc_name] = None
		for term in doc_terms[doc_name]:
			if term not in counts:
				counts[term] = 1
			else:
				counts[term] += 1 
				
		all_counts[doc_name] = counts
		# counts = sorted(counts.items(), key=operator.itemgetter(1))
	return all_counts

def parse(docs):
	'''
		Parse one document into a list of words
		 with only letters
		Return: Docs with term list
			{'doc1':['term1'...'termX'], 'doc2:..}
	'''
	terms = {}
	for d in docs: # Build list of terms for each doc
	# 	doc_terms.append(parse(d))
		doc_file = open(d)
		words = []
		regex = re.compile('[^a-zA-Z]')
		for i in doc_file.readlines():  # Split text to indiv. words
			temp_words = i.split()
			temp_words = [regex.sub('',w).lower() for w in temp_words]
			words.extend(temp_words)
		terms[d] = words
	return terms

def search(query, tfidfs):
	'''
		Inputs:  
			Query: List of words
			tfidfs: Tf-idf values for a set of terms in a set documents
				{'doc1':{'term1':(tf,idf,tfidf),..}, 'doc2':{...},...}
		Output:
			Document that has highest similarity for the query
				Computed based on vector similarity between query and doc vector
	'''
	pass
def main():
	docs = ["doc1","doc2","doc3","doc4","doc5"]
	docs = ["./"+i for i in docs]
	doc_terms = {}  # List of documents; each doc is list of terms
	tfs = [] 		# Term freq: Word count for each term in a doc
	doc_terms = parse(docs)
	tfs = get_tfs(doc_terms)
	# corpus_counts = count_all(tfs)
	idfs = get_idfs(tfs)
	tfidfs = get_tfidfs(tfs, idfs)
	# pp.pprint(tfidfs)

	query = ["oaths","kindness","love"]
	tophit = search(query,tfidfs)

main()