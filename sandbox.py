import re
a = "We will rock you.  Tonight."
regex = re.compile('[^a-zA-Z]')
#First parameter is the replacement, second parameter is your input string
b = a.split()
print b
c = [regex.sub('',i) for i in b]
print regex.sub('', a)
print c
#Out: 'abdE'