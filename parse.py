'''
parse.py
Parse for pagerank
'''
import json
import pickle
from pprint import pprint
pages = {}
counter = 0
path = "sitegraph-engr-9pm-7000.json"
with open(path) as inputfile:
	for line in inputfile:
		line = json.loads(line)		
		site = line['url']
		# Treat http and https as the same
		if site[4:5] == "s":
			site = site[5:]
		else:
			site = site[4:]
		links = line['linkedurls']
		links_dict = {}
		for l in links:
			# Deal with terminating "/"
			if (l[4:] not in links_dict and (l[4:]+"/") not in links_dict) and (l[5:] not in links_dict and (l[5:]+"/") not in links_dict):
				to_insert = {}
				if l[4:5] == "s":
					to_insert[l[5:]] = 0
					links_dict.update(to_insert)
				else:
					to_insert[l[4:]] = 0
					links_dict.update(to_insert)
		pages[site.encode('ascii','ignore')] = links_dict
		if counter % 1000 == 0:  # Progress track
			print counter
		counter += 1
outfile = open(path+".for_pr", "w")
pickle.dump(pages, outfile)
print "Done"
# pprint(pages)
