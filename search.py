# Search engine
from bs4 import BeautifulSoup
import urllib2
import urllib
import re
from pprint import pprint
import pickle
import json

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
	site = urllib2.urlopen(request, timeout=10)
	soup = BeautifulSoup(site, "html.parser")
	par = []
	for ptag in soup.find_all('p'):
		par.extend([ptag.get_text().encode('ascii','ignore')]) 
	return par 

def process_url(url):
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

def run_urls(urls):
	'''
		Input: List of URL strings
		Return: Collection of URLs with distinct terms
			{'www.site1.com':[word1,word2,...],...,'site2.com':...}
	'''
	url_terms = {}
	for url in urls:
		url_terms[url] =  process_url(url)
	pprint(url_terms)
	

urls = parse_feed('url_feed2')
run_urls(urls)