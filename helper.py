from __future__ import division
import pprint as pp
import re
import operator
from sets import Set

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

def get_doc_hits(query, inv_index, tfidfs):
	'''
		Inputs:  
			Query: List of words
			tfidfs: Tf-idf values for a Set of terms in a Set documents
				{'doc1':{'term1':(tf,idf,tfidf),..}, 'doc2':{...},...}
			Inverted index
		Output:
			Document that has highest similarity for the query
				Computed based on vector similarity between query and doc vector
	'''
	docs_to_get = Set()
	first = True
	for term in query:  
		if term in inv_index:
			temp_docs = inv_index[term]
			# print "term:", term
			# pp.pprint(temp_docs)
			if first:
				docs_to_get = temp_docs
				first = False
			else:
				docs_to_get = docs_to_get.union(temp_docs)  # For now, get set of docs that contain any of the query terms
	return docs_to_get

def get_inv_index(docs):
	'''
		Input: 
			Collection of documents and terms in each doc 
		Return:
			Inverted index 
				{'term1':['doc1','doc3'], 'term2':['doc3'], ...}
	'''
	inv_index = {}
	unique_terms = []
	for doc_name in docs:
		doc_set = Set()
		for term in docs[doc_name]:
			if term not in unique_terms:
				unique_terms.append(term)
				inv_index[term] = Set()
				inv_index[term].add(doc_name)
			else:
				inv_index[term].add(doc_name)
	# pp.pprint(inv_index)
	return inv_index

def get_scores(query,tophits,tfidfs):
	'''
		Inputs:
			query: list of terms in query
			tophits: set of docs whose score will be calculated based on query
			tfidfs: tfidf scores for each doc 
		Return:
			A score for each doc based on similarity with query
	'''
	scores = {}
	for doc_name in tophits:
		detailed = []
		doc_score = 0
		for term in query:
			if term in tfidfs[doc_name]:
				to_add = tfidfs[doc_name][term][2]
				doc_score = doc_score + to_add
				detailed.append([term,to_add,doc_score])
		scores[doc_name] = doc_score
		scores[doc_name] = detailed
	return scores

def doc_to_scores(docs):
	# docs = ["doc1","doc2","doc3","doc4","doc5"]
	docs = ["./"+i for i in docs]
	doc_terms = {}  # List of documents; each doc is list of terms
	tfs = [] 		# Term freq: Word count for each term in a doc
	doc_terms = parse(docs) # Collection of terms in docs without counts
	pp.pprint(doc_terms)
	inv_index = get_inv_index(doc_terms) # Inverted index (term -> doc1,doc2,)
	tfs = get_tfs(doc_terms)
	# corpus_counts = count_all(tfs)
	idfs = get_idfs(tfs)
	tfidfs = get_tfidfs(tfs, idfs)
	

	query = "In loving thee thou know'st I am forsworn Thus is his cheek the map of days outworn"
	query = query.split()
	tophits = get_doc_hits(query,inv_index,tfidfs)
	# print "query:",
	# pp.pprint(query)
	# print "doc hits:"
	# pp.pprint(tophits)
	scores = get_scores(query,tophits,tfidfs)
	pp.pprint(scores)

