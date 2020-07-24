def get_pivot_col_index(matrix):
	'''
		Search in z equation for the
		index with minor negative number
	'''
	
	return matrix[0].index(min(matrix[0]))

def get_pivot_row_index(matrix, col):
	'''
		Search in inequations for the
		index with minor positive number
	'''

	positive_rows = []
	# starts at inequations row
	i = 1
	# while there are inequations rows
	while i < ROW_LEN:
		# divide last col (b) by col (entering var or entering col)
		index, division = i, matrix[i][-1] / matrix[i][col]
		# only insert positive divisions cause we need minor positive number
		if division >= 0:
			positive_rows.append( (division, i) )
			
		i += 1

	# returns the min positive numbers index
	return min(positive_rows)[1]

def get_new_pivot_row(pivot_row, pivot_number):
	'''
		Return the new pivot row
		(pivot_row / pivot_number)
	'''

	return list(map(lambda number: number / pivot_number, pivot_row))

def get_new_row(new_pivot_row, inversed_var, row):
	multiplication = list(map(lambda number: number * inversed_var, new_pivot_row))
	new_row = []
	for m, n in zip(multiplication, row):
		new_row.append(m + n)
	
	return new_row

def get_new_matrix(matrix, pivot_row_index, new_pivot_row, pivot_col_index):
	'''
		Return new matrix, calculate new rows
	'''

	# just need to have already declared new matrix's indexes
	new_matrix = []
	for i in matrix:
		new_matrix.append([])

	i = 0
	while i < ROW_LEN:
		if i == pivot_row_index:
			i += 1
			continue

		new_row = get_new_row(new_pivot_row, matrix[i][pivot_col_index] * (-1), matrix[i])
		new_matrix[i] = new_row
		i += 1

	new_matrix[pivot_row_index] = new_pivot_row
	return new_matrix

def get_solution(matrix):
	not_basic_vars = []
	basic_vars = []

	# starting at inequations col
	j = 1
	# while not in b col
	while j < COL_LEN - 1:
		# starting at inequations row
		i = 1
		while i < ROW_LEN:
			if matrix[i][j] != 0 and matrix[i][j] != 1:
				not_basic_vars.append(j)
				break
			
			i += 1
		
		# if arrived at final row
		if i == ROW_LEN:
			basic_vars.append(j)

		j += 1

	return {
		'variáveis básicas': basic_vars,
		'variáveis não básicas': not_basic_vars,
		'valor de z': matrix[0][COL_LEN - 1]
	}

def is_optimal(z_eq):
	# start at vars
	i = 1
	# while not in b col
	while i < COL_LEN - 1:
		if z_eq[i] < 0:
			return False
		i += 1

	return True

def simplex(matrix):
	pivot_col_index = get_pivot_col_index(matrix)
	pivot_row_index = get_pivot_row_index(matrix, pivot_col_index)

	pivot_row = matrix[pivot_row_index]
	pivot_number = matrix[pivot_row_index][pivot_col_index]
	new_pivot_row = get_new_pivot_row(pivot_row, pivot_number)

	new_matrix = get_new_matrix(matrix, pivot_row_index, new_pivot_row, pivot_col_index)
	solution = get_solution(new_matrix)
	
	if is_optimal(new_matrix[0]):
		return solution
	
	return simplex(new_matrix)

# table = [
# 	[1, -10, -12, 0, 0, 0],
# 	[0, 1, 1, 1, 0, 100],
# 	[0, 1, 3, 0, 1, 270]
# ]

table = [
	[1, -3, -5, 0, 0, 0, 0],
	[0, 2, 4, 1, 0, 0, 10],
	[0, 6, 1, 0, 1, 0, 20],
	[0, 1, -1, 0, 0, 1, 30]
]

COL_LEN = table[0].__len__()
ROW_LEN = table.__len__()

solution = simplex(table)
print(solution)