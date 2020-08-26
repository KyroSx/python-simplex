from Simplex import Simplex

def main():
	# matrix of constraints
	constraints_matrix = [
		[ 1,  1, 1, 0, 0],
		[ 1, -1, 0, 1, 0],
		[-1,  1, 0, 0, 1]
	]
	# inequations sign column
	equationssign_column = ['<=', '<=', '<=']
	# inequations independent term: b column
	b_column = [6, 4, 4]

	# objective function coefficients
	f_list = [-1, -2, 0, 0, 0]
	# objective function value
	fx_value = 0
	# objective
	is_fmax = False
	is_fmin = True

	# list of basic indices (start 0)
	basic_indices = [2, 3, 4]
	# list of not basic indices (start 0)
	notbasic_indices = [0, 1]

	problem = Simplex(
		constraints_matrix,
		equationssign_column,
		b_column,
		is_fmax,
		is_fmin,
		f_list,
		fx_value,
		basic_indices,
		notbasic_indices
	)

	problem.run_simplex()



main()