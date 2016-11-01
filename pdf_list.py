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
	with open(input_file) as f:
		for line in f:
			line = json.loads(line)	
			site = [x.encode('ascii','ignore') for x in line['linkedurls'] 	]
			site = [x for x in site if x[-4:] == ".pdf"]
			pages.extend(site)
	pages = set(pages)
	pages = list(pages)
	return pages

path = "sitegraph-engr-730pm.json"
urls = get_urls_from_feed(path)
# pprint(urls[0][-4:])
pprint(urls)
pprint(len(urls))