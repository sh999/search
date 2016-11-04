'''
From JSON input of links, get unique PDF list to parse
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
	pages_and_pdf = {}  				# Dict of {pdf:site linking to pdf}; important to get the PR score of the linking site to infer PDF PR
	pages_and_pdf_data = path+".pdf_list"
	pages_and_pdf_data = open(pages_and_pdf_data,"w")
	with open(path) as f:
		for line in f:
			line = json.loads(line)	 	# JSON input = {site.html:out1.pdf,out2.html,out3.pdf,...}
			parent = line['url'].encode('ascii','ignore')  	# Site linking to the pdf
			# print parent
			pdf_site = [site.encode('ascii','ignore') for site in line['linkedurls']]
			pdf_site = [site for site in pdf_site if site[-4:] == ".pdf"]  	# Only care about .pdf. Can have a list of pdfs from one parent page
			for i in pdf_site:  		 
				pages_and_pdf[i] = parent 	# Build the dict of pdf:parent.html
			pdf_pages.extend(pdf_site)
	pickle.dump(pages_and_pdf,pages_and_pdf_data)  			# Save data for further processing; serve as list of pdfs to be parsed

	# pprint(pages_and_pdf)
	# pdf_pages = set(pdf_pages)
	# pdf_pages = list(pdf_pages)
	# return pdf_pages
	return pages_and_pdf

# path = "sitegraph-engr-730pm.json"
# path = "sitegraph-engr-9pm.json"
path = "sitegraph-engr-9pm-7000.json"  # Source JSON for pdf addresses to be parsed
urls = get_urls_from_feed(path)  	   # Get list of pdfs from above input file
pprint(len(urls))