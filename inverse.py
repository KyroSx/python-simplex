def matrix_transpose(m):
	return list(map(list, zip(*m)))

def matrix_minor(m, i, j):
	return [row[:j] + row[j + 1:] for row in (m[:i] + m[i + 1:])]

def matrix_determinant(m):
	# 2x2 matrix case
	if len(m) == 2:
		return m[0][0] * m[1][1] - m[0][1] * m[1][0]

	determinant = 0
	for i in range(len(m)):
		determinant += ((-1) ** i) * m[0][i] * matrix_determinant(matrix_minor(m, 0, i))
	
	return determinant

def matrix_inverse(m):
	determinant = matrix_determinant(m)
	# 2x2 matrix case:
	if m.__len__() == 2:
		return [
			[m[1][1] / determinant, -1 * m[0][1] / determinant],
			[-1 * m[1][0] / determinant, m[0][0] / determinant]
		]

	# find matrix of cofactors
	cofactors = []
	for r in range(len(m)):
		cofactorRow = []
		for c in range(len(m)):
			minor = matrix_minor(m, r, c)
			cofactorRow.append(((-1) ** (r + c)) * matrix_determinant(minor))
		cofactors.append(cofactorRow)
	
	cofactors = matrix_transpose(cofactors)
	
	for r in range(len(cofactors)):
		for c in range(len(cofactors)):
			cofactors[r][c] = cofactors[r][c] / determinant
	return cofactors

