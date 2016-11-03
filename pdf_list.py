'''
From JSON input, get unique PDF list
'''
import json
import pickle
from pprint import pprint
def get_urls_from_feed(path):
	'''
		Input: Path to json file with url link
		Return: Dict of pdf url:parent url (save as pickle)
	'''
	pdf_pages = []
	counter = 0
	pages_and_pdf = {}
	pages_and_pdf_data = path+".pdf_list"
	pages_and_pdf_data = open(pages_and_pdf_data,"w")
	with open(path) as f:
		for line in f:
			line = json.loads(line)	
			parent = line['url'].encode('ascii','ignore')
			# print parent
			pdf_site = [site.encode('ascii','ignore') for site in line['linkedurls'] 	]
			pdf_site = [site for site in pdf_site if site[-4:] == ".pdf"]
			for i in pdf_site:
				pages_and_pdf[i] = parent
			pdf_pages.extend(pdf_site)
	pickle.dump(pages_and_pdf,pages_and_pdf_data)

	# pprint(pages_and_pdf)
	# pdf_pages = set(pdf_pages)
	# pdf_pages = list(pdf_pages)
	# return pdf_pages
	return pages_and_pdf

# path = "sitegraph-engr-730pm.json"
# path = "sitegraph-engr-9pm.json"
path = "sitegraph-engr-9pm-7000.json"
urls = get_urls_from_feed(path)
# pprint(urls[0][-4:])
# pprint(urls)
pprint(len(urls))