import urllib2
from pprint import pprint
import pickle
class Cache:
	def __init__(self, urls):
		self.urls = urls
		self.url_flags = {}
		for i in self.urls:
			self.url_flags[i] = None

	def set_flag(self, url, flag):
		self.url_flags[url] = flag

	def print_all(self):
		# pprint(self.urls)
		pprint(self.url_flags)

def init_cache(out_path, urls):
	# urls = ['http://www.nytimes.com',
	# 		'http://www.wsj.com',
	# 		'http://en.wikipedia.org',
	# 		'http://www.yahoo.com,',
	# 		'http://www.microsoft.com',
	# 		'http://news.bbc.co.uk']
	url_cache = Cache(urls)
	for url in urls:
		# request = urllib2.Request(url)
		# try:
		# 	print "Requesting ", url, "..."
		# 	site = urllib2.urlopen(request, timeout = 0.2)
		# 	url_cache.set_flag(url,1)
		# 	print "\tSuccess"
		# except Exception, e:
		# 	print "\tFail"
		# 	print e
		# 	url_cache.set_flag(url,0)			
		url_cache.set_flag(url,0)
	url_cache.print_all()
	outfile = open(out_path,"w")
	pickle.dump(url_cache, outfile)
	outfile.close()
	print "Done"
def update_cache(cache_file):
	cache = pickle.load(open(cache_file,"r"))
	cache.print_all()
	unvisited = [k for k, v in cache.url_flags.items() if v == 0]
	pprint(unvisited)
	for url in unvisited:
		request = urllib2.Request(url)
		try:
			print "Requesting ", url, "..."
			site = urllib2.urlopen(request, timeout = 10)
			cache.set_flag(url,1)
			print "\tSuccess"
		except Exception, e:
			print "\tFail"
			print e
			cache.set_flag(url,0)	
	cache.print_all()


# init_cache(".cache1")
# update_cache(".cache1")