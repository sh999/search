# Search engine
from bs4 import BeautifulSoup
import urllib2
import re

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    # elif re.match('<!--.*-->', str(element)):
    elif re.match('<!--.*-->', element.encode('utf-8')):

        return False
    return True


def get_soup(url):
	request = urllib2.Request(url)
	site = urllib2.urlopen(request, timeout=3)
	site_soup = BeautifulSoup(site, "html.parser") 
	texts = site_soup.find_all(text=True)
	tag_a = site_soup.find_all("p")
	# for i in tag_a:
	# 	print i
	visible_texts = filter(visible, texts)
	print visible_texts[1:20]
	# for i in visible_texts:
	# 	try:
	# 		print i
	# 	except UnicodeEncodeError:
	# 		pass

url = "http://www.nytimes.com/"
get_soup(url)