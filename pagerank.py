'''
pagerank.py
Calculate pagerank given web graph
'''
import operator
from pprint import pprint
import copy
import pickle
def calc_unweighted(adj_list):
	'''
		Return adj list based on link presence; if link to a site, element is 1
	'''
	unweighted = copy.deepcopy(adj_list)
	for k, v in unweighted.iteritems():
		# print "site:", k
		# print "links:", v
		for name in v:
			v[name] = 1
		# print ""
	# pprint(unweighted)
	return unweighted

def calc_weighted(adj_list):
	'''
		Return adj list based on # of sites (vote dilution); if link to 3 sites, each element is 1/3
	'''
	# weighted = copy.deepcopy(adj_list)
	for k, v in adj_list.iteritems():
		# print "site:", k
		# print "# links:", len(v)
		# print "links:", v
		for name in v:
			v[name] = 1.0/len(v)
		# print ""
	# pprint(weighted)
	# return weighted
	return adj_list

def make_site_list(adj_list):
	'''
		Return a collection of unique sites from an adj_list of the web
	'''
	# print "Making site_list"
	site_list = {}
	num_id = 1				# Numerical id for each unique site
	# pprint(adj_list)
	for i in adj_list:
		# print "inserting i:",i
		if i not in site_list:
			# print "i not in site_list"
			site_list[i] = num_id
			num_id += 1
		for j in adj_list[i]:
			# print "inserting j:",j
			if j not in site_list:
				# print "j not in site_list"
				site_list[j] = num_id
				num_id += 1
			else:
				# print "j in site_list"
				pass
	# pprint(site_list)
	return site_list

def make_site_list_no_null(adj_list):
	'''
	Return a collection of unique sites from an adj_list of the web without null columns
	'''
	# print "Making site_list"
	site_list = {}
	num_id = 1				# Numerical id for each unique site
	# pprint(adj_list)
	for i in adj_list:
		# print "inserting i:",i
		if i not in site_list:
			# print "i not in site_list"
			site_list[i] = num_id
			num_id += 1
	# pprint(site_list)
	return site_list

def make_init_pr_vec_weighted(site_list):
	'''
		Make initial PageRank vector with values of 1/n
	'''
	i = 1.0/len(site_list)
	pr_vec = {}
	for pg in site_list:
		pr_vec[pg] = i 
		# i += 1
	# pr_vec = [1,2,3,4]
	# print "pr_vec:"
	# pprint(pr_vec)
	return pr_vec

def matrix_times_vector(damping, matrix, vector, dangling_sites):
	'''
		One iteration of the pagerank calculation
	'''
	# print "matrix_times_vector:"
	# print "damping:", damping
	# pprint(matrix)
	# pprint(vector)
	pr_vector = {}	
	null_sum = 0
	factor = 1.0/len(vector)*damping
	# print "Factor:", factor
	for d in dangling_sites:
		# print "Adding dangling site:", d
		null_sum = null_sum + vector[d] * factor
	# print "null_sum:", null_sum
	for row in vector:						# Loop through result vector
		# print "\npr row:", row
		curr_sum = 0
		if row in matrix:
			# print "matrix[row]:", matrix[row]
			for elem in matrix[row]:		# Loop through matrix row	
				# print "multiplying", elem, ":", matrix[row][elem], "by", vector[elem]
				mult = matrix[row][elem] * vector[elem]		# Multiply matrix row by vector column
				curr_sum += mult 			# Sum terms successively
			# print "curr_sum:", curr_sum
		pr_vector[row] = curr_sum + null_sum
	# print "Multiplying/adding null terms:"
	# print "result of Matrix times vector:"
	# pprint(pr_vector)
	return pr_vector

def rotate(matrix):
	'''
		Given matrix with rows X and cols Y, return a matrix
		 with rows Y and cols X. Necessary for pagerank to convert
		 original adj. list
	'''
	# print "in rotate()"
	rotated = {}
	# pprint(matrix)
	for k, v in matrix.iteritems():
		# print "ITEM",k
		for i in v:
			# print "i:",i," k:",k
			# print "orig:", matrix[k][i]
			to_insert = {}
			to_insert[k] = matrix[k][i]
			# print "to insert:"
			# pprint(to_insert)
			if i not in rotated:
				rotated[i] = {}
			rotated[i].update(to_insert) 
	return rotated

def scalar_times_matrix(scalar, matrix):
	'''
		Multiply scalar times matrix.
		Important for, say, alpha times S 
	'''
	# print "Multiplying scalar and matrix below:"
	# print scalar
	# pprint(matrix)
	result = {}
	# pprint(matrix)
	for k, v in matrix.iteritems(): 	# Loop through matrix row elements
		# print "k:", k
		to_insert = {} 					# Temporary row element to insert
		for i in v: 					# Loop through columns
			to_insert[i] = scalar * matrix[k][i] 	# Multiply same scalar by each element for all elements in row
			# print "\tto_insert\t",
			# pprint(to_insert)
			to_insert.update(to_insert) 	# Putative row to insert
			# print ""
		result[k] = to_insert 			# Insert multiple elements (row)
	return result

def surfer_times_pr(inv_damping,vector):
	'''
		Multiplies "Matrix" of random surfer (term 2 of equation)
		 by pagerank vector
		But not really storing surfer matrix because it's full
		Instead, multiply element by element
	'''
	sum_of_vec_elements = 0
	for k in vector:
		sum_of_vec_elements = sum_of_vec_elements + vector[k]
	factor = sum_of_vec_elements * inv_damping / len(vector)	
	# print "sum:", sum_of_vec_elements
	return factor

def add_vectors(vector1, vector2):
	'''
		After distributing the pr vectors, add them together
		vector2 is not really a vector; it's a number but represents vector
		 filled with the same number
	'''
	result = {}
	for k in vector1:
		# print "k:", k
		# print "vector1[k]:", vector1[k]
		result[k] = vector1[k] + vector2
	return result

def one_iteration(damping, matrix, pr_vector, dangling_sites):
	new_pr_vector = {}
	inv_damping = 1 - damping
	print "Calculating weighted matrix..."
	weighted = calc_weighted(matrix)  	 # Get adj list of raw numbers (1 = outlinks to)
	print "Rotating weighted matrix..."
	rotated_weighted = rotate(weighted)		 # Rotate weighted adj list to proper form
	# pprint(rotated_weighted)
	print "Applying damping to matrix..."
	rotated_weighted_damping = scalar_times_matrix(damping,rotated_weighted)		 # Multiply weighted matrix by damping factor (alpha * S)
	# pprint(rotated_weighted_damping)
	print "Multiplying matrix with pr vector..."
	term1 = matrix_times_vector(damping, rotated_weighted_damping, pr_vector, dangling_sites)
	print "Applying surfer model..."
	term2 = surfer_times_pr(inv_damping,pr_vector)
	print "Final addition..."
	added = add_vectors(term1,term2)
	return added

def sum_vector(vector):
	'''
		To check if pr values add up to 1
	'''
	summed = 0
	for i in vector:
		summed += vector[i]
	return summed

def fill_null_columns(adj_list, pr_vector):
	'''
		Fill null clolumns
	'''
	# print "Finding null column:"
	# print "adj list:"
	# pprint(adj_list)
	# print "pr_vector:"
	# pprint(pr_vector)
	# print "keys in adj_list:"
	to_insert = {}
	for key in pr_vector:
		to_insert[key] = 0
	for key in pr_vector:
		if key not in adj_list:
			adj_list[key] = to_insert
	# print "new adj_list"
	# pprint(adj_list)
	# print "End finding null column"
	return adj_list

def delete_null_columns(adj_list, pr_vector):
	'''
		Delete outlinks to not include dangling links
	'''
	new_list = {}
	for i in adj_list:
		for j in adj_list[i].keys():
			if j not in pr_vector:
				# print j, "is not in pr_vector"
				del adj_list[i][j]

def find_dangling(pr_vector, adj_list):
	'''
		Find dangling_sites. Useful for dealing with null columns later
	'''
	dangling_sites = []
	for i in pr_vector:
		# print i
		if i not in adj_list:
			# print "not"
			dangling_sites.append(i)
	# pprint(dangling_sites)
	return dangling_sites

def calc_dist(vec1, vec2):
	'''
		Calculates distance between two vectors with same elements
	'''
	diff = 0
	for i in vec1:
		diff += abs(vec2[i] - vec1[i])
	return diff

def main():	
	damping = 0.85
	source = "sitegraph-engr-9pm-7000.json.for_pr"
	infile = open(source, "r")
	print "Loading pickle object..."
	pr_out = "sitegraph-engr-9pm-7000.json.pr"
	adj_list = pickle.load(infile)
	'''
		Below lists are the three simple test cases
	'''
	# adj_list = {"A":{"B":0,"C":0}, "B":{"C":0},"C":{"A":0},"D":{"C":0}}
	# adj_list = {"Home":{"About":0,"Products":0,"Links":0}, "About":{"Home":0},"Products":{"Home":0},"Links":{"Home":0,"ExtA":0,"ExtB":0,"ExtC":0,"ExtD":0,}}
	# adj_list = {"Home":{"About":0,"Products":0,"Links":0}, "About":{"Home":0},"Products":{"Home":0},"Links":{"Home":0,"ExtA":0,"ExtB":0,"ExtC":0,"ExtD":0,"RevA":0,"RevB":0,"RevC":0,"RevD":0},"RevA":{"Home":0},"RevB":{"Home":0},"RevC":{"Home":0},"RevD":{"Home":0}}
	# print "Making initial pr vector..."
	pr_vector = make_init_pr_vec_weighted(make_site_list(adj_list))  # Make initial PageRank vector with 1/n as value for each element
	dangling_sites = find_dangling(pr_vector, adj_list)  			 # Find sites that are dangling (null columns)
	# pr_vector = make_init_pr_vec_weighted(make_site_list_no_null(adj_list))
	# pprint(pr_vector)
	# print "Filling null columns..."
	# adj_list = fill_null_columns(adj_list, pr_vector)
	# print "Deleting null columns..."
	# delete_null_columns(adj_list, pr_vector)
	# pprint(adj_list)
	print "Iterating..."
	pr = one_iteration(damping, adj_list, pr_vector, dangling_sites) # First iteration
	# print "\norig pr:"
	limit = 50 			# Limit of iteration numbers
	iterations = 0 			
	prev_pr = pr 			# Save previous PR to compare distance after each iteration
	convergence = 0.000001 	# If distance between previous and current PR is < this, end program
	while(iterations < limit):
		# print "\n-------------"
		# print "\nRun iteration ", iterations
		# print "Pr before:"
		# pprint(pr)
		print "# ", iterations
		pr = one_iteration(damping, adj_list, pr, dangling_sites) 	# Calculate new PageRank
		dist = calc_dist(pr, prev_pr) 								# Distance to previous PR
		print "dist to prev vec:", dist
		if dist < convergence: 			# End if convergence is seen
			break
		# print "Pr after:"
		# pprint(pr)
		prev_pr = pr
		iterations += 1
	print "Damping:", damping
	print "Convergence limit:", convergence
	print "# Iterations:", iterations
	new_pr = {}
	for key in pr:
		new_pr[key.encode('ascii','ignore')] = pr[key]
	sorted_pr = sorted(new_pr.items(), key=operator.itemgetter(1))
	pr_out = open(pr_out,"w")
	pr_out = pickle.dump(pr,pr_out)
	pprint(sorted_pr[-10:])
	# for i in sorted_pr:
	# 	print type(i[0]),type(i[1])
	print "Sum:", sum_vector(pr)
	infile.close()
	print "Done"

main()