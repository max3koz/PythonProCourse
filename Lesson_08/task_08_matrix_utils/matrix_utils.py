from typing import List


def transpose_matrix(matrix: List[List[int]]) -> List[List[int]]:
	"""
	Transposes the matrix (rows become columns).
	>>> transpose_matrix([[1, 2], [3, 4]])
	[[1, 3], [2, 4]]
	>>> transpose_matrix([[1, 2, 3], [4, 5, 6]])
	[[1, 4], [2, 5], [3, 6]]
	>>> transpose_matrix([[7]])
	[[7]]
	>>> transpose_matrix([])
	[]
	"""
	return list(map(list, zip(*matrix)))


def matrix_multiply(matrix1: List[List[int]], matrix2: List[List[int]]) -> List[
	List[int]]:
	"""
	Multiplies two matrices (matrix1 × matrix2).
	>>> matrix_multiply([[1, 2], [3, 4]], [[5, 6], [7, 8]])
	[[19, 22], [43, 50]]
	>>> matrix_multiply([[2, 0], [0, 2]], [[1, 2], [3, 4]])
	[[2, 4], [6, 8]]
	>>> matrix_multiply([[1, 2, 3]], [[4], [5], [6]])
	[[32]]
	>>> matrix_multiply([[1]], [[2]])
	[[2]]
	>>> matrix_multiply([], [])
	[]
	"""
	if not matrix1 or not matrix2:
		return []
	
	rows_a = len(matrix1)
	cols_a = len(matrix1[0])
	rows_b = len(matrix2)
	cols_b = len(matrix2[0])
	
	if cols_a != rows_b:
		raise ValueError("The number of columns in the first matrix must be "
		                 "equal to the number of rows in the second matrix.")
	
	result = [[0 for _ in range(cols_b)] for _ in range(rows_a)]
	
	for i in range(rows_a):
		for j in range(cols_b):
			for k in range(cols_a):
				result[i][j] += matrix1[i][k] * matrix2[k][j]
	
	return result
