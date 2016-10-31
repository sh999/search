# Search engine
from bs4 import BeautifulSoup
import urllib2
import urllib
import re
from pprint import pprint
import pickle
import json
from helper import *

def get_terms(text):
	'''
		Input:
			text: list of strings, each may be a paragraph 
		Return: 
			list of distinct terms/words
	'''
	s = []
	regex = re.compile('[^a-zA-Z]')
	for t in text:
		t = t.split()
		t = [x.encode('ascii','ignore') for x in t]
		t = [regex.sub('',w).lower() for w in t]
		s.extend(t)
	# text = [x.encode('ascii','ignore') for x in text]
	stops = ['the', 'a', 'in','of','as','and','on','to',
			 'by','was','is','are','am','an','be']
	s = [x for x in s if x != '' and x not in stops]
	return s

def get_pars(url):
	'''
		Given URL, get HTML, parse for <p> text,
		return list of paragraphs 
	'''
	request = urllib2.Request(url)
	par = []
	try:
		site = urllib2.urlopen(request, timeout=4)
		soup = BeautifulSoup(site, "html.parser")
	except Exception:
		return par
	for ptag in soup.find_all('p'):
		par.extend([ptag.get_text().encode('ascii','ignore')]) 
	return par 

def get_terms_from_url(url):
	'''
		Input: URL
		Return: List of terms in URL's html
	'''
	# url = 'https://www.en.wikipedia.org'
	par = get_pars(url)
	terms = get_terms(par)
	return terms

def parse_feed(input_file):
	'''
		Input: Path to json file with url link
		Return: List of urls
	'''
	pages = []
	counter = 0
	with open(input_file) as f:
		for line in f:
			line = json.loads(line)	
			site = line['url'].encode('ascii','ignore')	
			pages.extend([site])
	return pages


def run_urls(urls, need_tfidfs):
	'''
		Input: List of URL strings
		Return: Collection of URLs with distinct terms
			{'www.site1.com':[word1,word2,...],...,'site2.com':...}
	'''
	url_terms = {}
	print "Processing URLS to get terms..."
	counter = 0
	for url in urls:
		url_terms[url] =  get_terms_from_url(url)
		counter += 1
		if counter % 1 == 0:
			print counter
	# pprint(url_terms)
	print "Calculating tfidfs..."
	tfs = [] 		# Term freq: Word count for each term in a doc
	inv_index = get_inv_index(url_terms) # Inverted index (term -> doc1,doc2,)
	tfs = get_tfs(url_terms)
	# corpus_counts = count_all(tfs)
	idfs = get_idfs(tfs)
	tfidfs = get_tfidfs(tfs, idfs)
	

	# pprint(tfidfs)
	print "Searching docs with query..."
	query = "software engineering with best practices and rigorous standards"
	query = query.split()
	tophits = get_doc_hits(query,inv_index,tfidfs)
	# print "query:",
	# pp.pprint(query)
	# print "doc hits:"
	# pp.pprint(tophits)
	scores = get_scores(query,tophits,tfidfs)
	pp.pprint(scores)

raw_feed = "sitegraph-engr-730pm.json"
# raw_feed = "url_feed"
need_tfidfs = True  
urls = parse_feed(raw_feed)
print(len(urls))
run_urls(urls, need_tfidfs)
