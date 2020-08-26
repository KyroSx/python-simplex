from inverse import matrix_inverse

def dot_product(list1, list2):
	''' Returns a scalar, wich is the sum of each list elements product
		(list1, list2)
	'''
	
	product = 0
	for l1, l2 in zip(list1, list2):
		product += l1 * l2
	return product

class Simplex:
	def __init__(
		self,
		constraints_matrix,
		equationssign_column,
		b_column,
		is_fmax,
		is_fmin,
		f_list,
		fx_value,
		basic_column_indices,
		notbasic_column_indices
	):
		self.constraints_matrix = constraints_matrix
		self.equationssign_column = equationssign_column
		self.b_column = b_column
		self.is_fmax = is_fmax
		self.is_fmin = is_fmin
		self.f_list = f_list
		self.fx_value = fx_value
		self.basic_column_indices = basic_column_indices
		self.notbasic_column_indices = notbasic_column_indices

	def run_show_problem(self):
		print('problema:')
		if self.is_fmax:
			print('max f(x) = ', end='')
		elif self.is_fmin:
			print('min f(x) = ', end='')
		
		for i in range(len(self.f_list)):
			print(f'{self.f_list[i]}x{i + 1} ', end='')
		
		print()
		for constraint, sign, b in zip(
			self.constraints_matrix,
			self.equationssign_column,
			self.b_column
		):
			print('\t', end='')
			for i in range(len(constraint)):
				print(f'{constraint[i]}x{i + 1} ', end='')
			print(f'{sign} {b}')
		print()

	def run_is_fmax(self):
		if self.is_fmax:
			self.is_fmax = False
			self.is_fmin = True
			self.f_list = list_scalarproduct(self.f_list, -1)

	def run_invert_sign(self, index):
		if self.equationssign_column[index] == '>=':
			self.equationssign_column[index] = '<='
		elif self.equationssign_column[index] == '<=':
			self.equationssign_column[index] = '>='
		elif self.equationssign_column[index] == '>':
			self.equationssign_column[index] = '<'
		elif self.equationssign_column[index] == '<':
			self.equationssign_column[index] = '>'
		elif self.equationssign_column[index] == '=':
			self.equationssign_column[index] = 'unrestricted'
		elif self.equationssign_column[index] == 'unrestricted':
			self.equationssign_column[index] = '='
	
	def run_thereis_blt0(self):
		for i in range(len(self.b_column)):
			if self.b_column[i] < 0:
				self.b_column[i] *= -1
				self.constraints_matrix[i] = list_scalarproduct(
					self.constraints_matrix[i], -1
				)
				self.run_invert_sign(i)

	def needs_phase1(self):
		return \
			'>' in self.equationssign_column or \
			'>=' in self.equationssign_column or \
			'=' in self.equationssign_column

	def run_phase1(self):
		pass

	def create_basic_matrix(self):
		basic_matrix = [
			[ 0 for j in self.basic_column_indices ] \
			for i in self.constraints_matrix
		]

		for k, j in zip(self.basic_column_indices, range(len(self.basic_column_indices))):
			for i in range(len(self.constraints_matrix)):
				basic_matrix[i][j] = self.constraints_matrix[i][k]

		return basic_matrix

	def get_basic_solution(self, basic_matrix_inverse):
		basic_solution = []
		for i in range(len(basic_matrix_inverse)):
			acumulator = 0
			for j in range(len(basic_matrix_inverse[0])):
				acumulator += basic_matrix_inverse[i][j] * self.b_column[j]
			basic_solution.append(acumulator)

		return basic_solution

	def get_relative_costs(self, basic_matrix_inverse):
		## passo 2.1 ##
		lambda_list = []
		for i, k in zip(range(len(basic_matrix_inverse)), self.basic_column_indices):
			acumulator = 0
			for j in range(len(self.basic_column_indices)):
				acumulator += basic_matrix_inverse[i][j] * self.f_list[k]
			lambda_list.append(acumulator)
		## passo 2.1 ##

		# print(lambda_list)
		## passo 2.2 ##
		relative_costs = []
		for j in self.notbasic_column_indices:
			column = []
			for i in range(len(self.constraints_matrix)):
				column.append(self.constraints_matrix[i][j])
			
			relative_costs.append({
				'value': self.f_list[j] - dot_product(lambda_list, column),
				'index': j
			})
		## passo 2.2 ##

		## passo 2.3 ##
		minor = min(relative_costs, key=lambda c: c['value'])
		## passo 2.3 ##

		return {
			'index': minor['index'],
			'value': minor['value'],
			'end': minor['value'] >= 0
		}

	def get_y(self, i, basic_matrix_inverse):
		column = []
		for l in range(len(self.constraints_matrix)):
			column.append(self.constraints_matrix[l][i])

		y = []
		for row in basic_matrix_inverse:
			acumulator = 0
			for b, a in zip(row, column):
				acumulator += b * a
			y.append(acumulator)

		return y

	def get_epsilon(self, y, xhat_b):
		minimum = 9999999999999999999
		minimum_i = ''
		for i in range(len(y)):
			if y[i] > 0 and xhat_b[i] >= 0 and minimum > (xhat_b[i] / y[i]):
				minimum = xhat_b[i] / y[i]
				minimum_i = i
		
		return {
			'value': minimum,
			'index': self.basic_column_indices[minimum_i],
			'end': minimum == 9999999999999999999
		}

	def run_switch_columns(self, notbasic, basic):
		nb = notbasic['index']
		b = basic['index']
		# troca as colunas das restrições
		# for i in range(len(self.constraints_matrix)):
		# 	aux = self.constraints_matrix[i][nb]
		# 	self.constraints_matrix[i][nb] = self.constraints_matrix[i][b]
		# 	self.constraints_matrix[i][b] = aux
		
		# troca os coeficientes da função objetivo
		# aux = self.f_list[nb]
		# self.f_list[nb] = self.f_list[b]
		# self.f_list[b] = aux
		
		# trocar os índices das variáveis
		self.notbasic_column_indices.remove(nb)
		self.notbasic_column_indices.append(b)
		self.basic_column_indices.remove(b)
		self.basic_column_indices.append(nb)

		# atualiza o f(x)
		self.fx_value = self.fx_value + notbasic['value'] * basic['value']

	def run_phase2(self):
		basic_matrix = self.create_basic_matrix()
		basic_matrix_inverse = matrix_inverse(basic_matrix)

		## passo 1 ##
		# x^B
		xhat_b = self.get_basic_solution(basic_matrix_inverse)
		# print(basic_matrix)
		# x^N
		xhat_n = [0] * len(self.notbasic_column_indices)
		## passo 1 ##

		## passo 2 ##
		chat_n = self.get_relative_costs(basic_matrix_inverse)
		## passo 2 ##
		
		## passo 3 ##
		if chat_n['end'] == True:
			print('solução:')
			for b, xb in zip(self.basic_column_indices, xhat_b):
				print(f'{{x{b + 1} = {xb}}}')
			for n, xn in zip(self.notbasic_column_indices, xhat_n):
				print(f'{{x{n + 1} = {xn}}}')
			print(f'fx = {self.fx_value}')
			return False
		## passo 3 ##
		
		## passo 4 ##
		y = self.get_y(chat_n['index'], basic_matrix_inverse)
		## passo 4 ##
		
		## passo 5 ##
		epsilon = self.get_epsilon(y, xhat_b)
		if epsilon['end'] == True:
			print('solução negativa infinita')
			return False
		## passo 5 ##
		
		## passo 6 ##
		self.run_switch_columns(chat_n, epsilon)
		## passo 6 ##

		return True
		
	def run_simplex(self):
		self.run_show_problem()
		
		## verificação da necessidade da Fase I ##
		self.run_is_fmax()
		self.run_thereis_blt0()

		if self.needs_phase1():
			self.run_phase1()
		## verificação da necessidade da Fase I ##
		
		i = 1
		while self.run_phase2():
			i += 1
		print(f'\n{i} iterações')