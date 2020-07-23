def get_pivot_col(matrix):
	'''
		Search in z equation for the
		index of minor negative number
	'''
	
	return matrix[0].index(min(matrix[0]))

def get_pivot_row(matrix, col):
	'''
		Search in inequations for the
		index of minor positive number
	'''

	COL_LEN = matrix[0].__len__()
	ROW_LEN = matrix.__len__()
	
	positive_rows = []
	# start in inequations row
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

def simplex(matrix):
	col = get_entering_col(matrix)
	row = get_outing_row(matrix, col)
	print(col, row)

table = [
	[1, -10, -12, 0, 0, 0],
	[0, 1, 1, 1, 0, 100],
	[0, 1, 3, 0, 1, 270]
]

simplex(table)