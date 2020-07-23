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

	COL_LEN = matrix[0].__len__()
	ROW_LEN = matrix.__len__()
	
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

	COL_LEN = matrix[0].__len__()
	ROW_LEN = matrix.__len__()

	# just need to have already declared new matrix's indexes
	new_matrix = []
	for i in matrix:
		new_matrix.append([])

	i = 0
	while i < ROW_LEN and i != pivot_row_index:
		new_row = get_new_row(new_pivot_row, matrix[i][pivot_col_index] * (-1), matrix[i])
		new_matrix[i] = new_row
		i += 1

	new_matrix[pivot_row_index] = new_pivot_row
	return new_matrix

def simplex(matrix):
	pivot_col_index = get_pivot_col_index(matrix)
	pivot_row_index = get_pivot_row_index(matrix, pivot_col_index)

	pivot_row = matrix[pivot_row_index]
	pivot_number = matrix[pivot_row_index][pivot_col_index]
	new_pivot_row = get_new_pivot_row(pivot_row, pivot_number)

	new_matrix = get_new_matrix(matrix, pivot_row_index, new_pivot_row, pivot_col_index)
	print(new_matrix)

table = [
	[1, -10, -12, 0, 0, 0],
	[0, 1, 1, 1, 0, 100],
	[0, 1, 3, 0, 1, 270]
]

simplex(table)