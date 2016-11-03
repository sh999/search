import re
from sets import Set
import urllib2
from bs4 import BeautifulSoup
from pprint import pprint
import json
import pickle
import slate
import os
import ssl
def re_test():
	a = "We will rock you.  Tonight."
	regex = re.compile('[^a-zA-Z]')
	#First parameter is the replacement, second parameter is your input string
	b = a.split()
	print b
	c = [regex.sub('',i) for i in b]
	print regex.sub('', a)
	print c
	#Out: 'abdE'

def set_test():
	a = Set([1,2,3])
	b = Set([2,3,4])
	print a.intersection(b)

def split_test():
	a = "hey there"
	b = "hey"
	print(a.split())
	print(b.split())
def soup_test():
	url = 'https://en.wikipedia.org/wiki/Occult'
	request = urllib2.Request(url)
	site = urllib2.urlopen(request, timeout=3)
	soup = BeautifulSoup(site, "html.parser")
	# pp.pprint(soup)
	print(type(soup))
	par = []
	for ptag in soup.find_all('p'):
		print type(ptag.get_text().encode('ascii','ignore'))
		par.extend([ptag.get_text().encode('ascii','ignore')]) 
	# pp.pprint(a)
	print(len(par))
def json_test():
	pages = []
	counter = 0
	with open("url_feed") as f:
		for line in f:
			line = json.loads(line)	
			site = line['url'].encode('ascii','ignore')	
			pages.extend([site])
	print(pages)
	outfile = open("out", "w")
	pickle.dump(pages, outfile)
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
		# t = [x.encode('ascii','ignore') for x in t]
		t = [regex.sub('',w).lower() for w in t]
		t = [w for w in t if len(w) > 3]
		s.extend(t)
	# text = [x.encode('ascii','ignore') for x in text]
	stops = ['the', 'a', 'in','of','as','and','on','to',
			 'by','was','is','are','am','an','be']
	s = [x for x in s if x != '' and x not in stops]
	return s
def parse_pdf(filepath):
	print "Parsing pdf..."
	with open(filepath, 'rb') as inputfile:
		try:
			doc = slate.PDF(inputfile)
			# for i in doc:
				# print type(i)
				# print i
			# words = [x.encode('ascii','ignore') for x in doc]
			# words = [w for w in doc]
			# pp.pprint(words)
			terms = get_terms(doc)
			# for i in terms:
			# 	print i
			return terms
		except Exception, error:
			print error
			pass
def get_size(url):
	f = urllib2.urlopen(url)
	size= f.headers["Content-Length"]
	print size
def get_pdfs(pdf_list):
	'''
		Given list of urls to pdf files, process them
	'''
	# print pdf_list
	for pdf in pdf_list:
		f = urllib2.urlopen(pdf)
		try:
			size = f.headers["Content-Length"]
			print size
		except KeyError, error:
			print error
			pass
		except urllib2.HTTPError, error:
			print error
			pass

def urllib_pdf():
	# directly read bytes from file url
	# won't work with search
	url = 'http://www.engr.uky.edu/me/files/2011/05/WMR_4-12-07.pdf'
	f = urllib2.urlopen(url)
	s = f.read()
	print s[1:400]
	# print type(s)
	# print s
def download(pdf_list):
	# download pdf file
	doc_terms = {}
	for i in pdf_list:
		try:
			f = urllib2.urlopen(i, timeout=0.5)
			temp_pdf = './pdf/dl.pdf'
			with open(temp_pdf,'wb') as output:
			  output.write(f.read())
			# parse_pdf(temp_pdf)
			doc_terms[i] = parse_pdf(temp_pdf)
			os.remove(temp_pdf)
		except urllib2.HTTPError, error:
			print error
			pass
		except ssl.SSLError, error:
			print error
			pass
	pprint(doc_terms)
def pdf_list_load():
	f = "sitegraph-engr-9pm-7000.json.pdf_list"
	f = open(f,"r")
	f = pickle.load(f)
	pprint(f)
def download_pdfs():
	data = "sitegraph-engr-9pm-7000.json.pdf_list"
	data = open(data,"r")
	data = pickle.load(data)
	pdf_list = data.keys()
	pprint(pdf_list)
	download(pdf_list[0:4])
	# pprint(data)


download_pdfs()