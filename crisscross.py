import numpy as np
from sympy import *
from copy import copy

def get_starting_basis(m, n, A_b):
	transformed_A_b = A_b.rref()
	pivot_positions = transformed_A_b[1]
	row_echelon_A_b = transformed_A_b[0]

	if (len(pivot_positions) != m):
		row_echelon_A_b = row_echelon_A_b[0:len(pivot_positions), 0:(n+m+1)]

	return([row_echelon_A_b, pivot_positions])

def precheck_feasibility(starting_basis, pivot_positions):
	nr_cols = starting_basis.shape[1]

	if ((nr_cols-1) in pivot_positions):
		return(False)
	else:
		return(True)

def criss_cross(m, n, A_b):
	pivot_tables = []
	pivot_positions = []
	basis_variables = []

	starting_basis = get_starting_basis(m, n, A_b)

	basic_solution_indices = starting_basis[1]
	current_basis = starting_basis[0]

	basis_variables.append(copy(basic_solution_indices))
	pivot_tables.append(current_basis)

	if (not precheck_feasibility(current_basis, basic_solution_indices)):
		return([-1, pivot_positions, pivot_tables, basis_variables])

	while True:

		if all(b >= 0 for b in current_basis.col(-1)):
			print "Feasible solution found..."
			return([0, pivot_positions, pivot_tables, basis_variables])
			break

		min_index_row = next((i for i in xrange(0,len(current_basis.col(-1))) if current_basis.col(-1)[i] < 0), -1)
		print(min_index_row)
		min_index_col = next((i for i in xrange(0,(len(current_basis.row(min_index_row))-1)) if current_basis.row(min_index_row)[i] < 0), -1)
		print(min_index_col)

		if (min_index_col == -1):
			print "It is primal infeasible..."
			return([-1, pivot_positions, pivot_tables, basis_variables])
			break

		pivot_positions.append((min_index_row, min_index_col))

		basic_solution_indices[min_index_row] = min_index_col
		current_basis = current_basis[0:m, basic_solution_indices].inv()*current_basis
		
		basis_variables.append(copy(basic_solution_indices))
		pivot_tables.append(current_basis)