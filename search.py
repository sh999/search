# Search engine
from bs4 import BeautifulSoup
import urllib2
import urllib

import re
from pprint import pprint

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    # elif re.match('<!--.*-->', str(element)):
    elif re.match('<!--.*-->', element.encode('utf-8')):

        return False
    return True

def parse(inputstring):
	'''
		Parse one document into a list of words
		 with only letters
		Return: Docs with term list
			{'doc1':['term1'...'termX'], 'doc2:..}
	'''
	terms = inputstring.split()
	terms = [x.encode('ascii','ignore') for x in terms]
	return terms

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
	return par 

def get_soup(url):
	request = urllib2.Request(url)
	site = urllib2.urlopen(request, timeout=3)
	site_soup = BeautifulSoup(site, "html.parser") 
	# texts = site_soup.find_all("p").getText()
	texts = site_soup.get_text()
	# print texts
	return texts
	# texts = site_soup.find_all("p")
	# print(texts)
	# for i in tag_a:
	# 	print i
	visible_texts = filter(visible, texts)
	# print visible_texts[1:20]
	# for i in visible_texts:
	# 	try:
	# 		print i
	# 	except UnicodeEncodeError:
	# 		pass
	return visible_texts

def get_html(url):
	request = urllib2.Request(url)
	site = urllib2.urlopen(request, timeout=3)
	site_soup = BeautifulSoup(site, "html.parser") 
	texts = site_soup.find_all(text=True)
	tag_a = site_soup.find_all("p")
	texts = site_soup.find_all()

	return texts

def get2(url):
	try:
		html = urllib.urlopen(url).read()
		soup = BeautifulSoup(html)
		# kill all script and style elements
		for script in soup(["script", "style"]):
		    script.extract()    # rip it out
		# get text
		text = soup.get_text()
		# break into lines and remove leading and trailing space on each
		lines = (line for line in text.splitlines())
		# lines = (line.strip() for line in text.splitlines())
		# break multi-headlines into a line each
		chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
		# drop blank lines
		text = '\n'.join(chunk for chunk in chunks if chunk)
	except UnicodeEncodeError:
		pass
	return text

url = 'https://www.engr.uky.edu/visit/'
par = get_pars(url)
terms = get_terms(par)
pprint(terms)
pprint(len(terms))
