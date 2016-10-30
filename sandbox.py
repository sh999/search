import re
from sets import Set
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

set_test()