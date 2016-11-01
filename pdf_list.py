'''
From JSON input, get unique PDF list
'''
import json
from pprint import pprint
def get_urls_from_feed(input_file):
	'''
		Input: Path to json file with url link
		Return: List of urls
	'''
	pages = []
	counter = 0
	pages_and_pdf = {}
	with open(input_file) as f:
		for line in f:
			line = json.loads(line)	
			pdf_site = [site.encode('ascii','ignore') for site in line['linkedurls'] 	]
			pdf_site = [site for site in pdf_site if site[-4:] == ".pdf"]
			pages.extend(pdf_site)

	pages = set(pages)
	pages = list(pages)
	return pages
def get_urls_from_feed2(input_file):
	'''
		Input: Path to json file with url link
		Return: List of urls
	'''
	pages = []
	counter = 0
	pages_and_pdf = {}
	with open(input_file) as f:
		for line in f:
			line = json.loads(line)	
			# pdf_site = [site.encode('ascii','ignore') for site in line['linkedurls'] 	]
			# pdf_site = [site for site in pdf_site if site[-4:] == ".pdf"]
			# pages.extend(pdf_site)
			for site in line['linkedurls']:

				if site[-4:] == ".pdf":
					pages_and_pdf[line['url'].encode('ascii','ignore')] = site.encode('ascii','ignore')

	return pages_and_pdf

path = "sitegraph-engr-730pm.json"
# path = "sitegraph-engr-9pm.json"

urls = get_urls_from_feed(path)
# pprint(urls[0][-4:])
pprint(urls)
pprint(len(urls))