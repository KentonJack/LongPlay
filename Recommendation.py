def matrix_mul(a, b):
	result = [[0] * len(b[0]) for i in range(len(a))]
	for i in range(len(a)):
		for j in range(len(b[0])):
			for k in range(len(b)):
				result[i][j] += a[i][k] * b[k][j]
	return result


A = [[2, 0, 0]]
i = 0
with open('info/record.txt', 'r') as f:
	for line in f.readlines():
		A[0][i] = int(line.strip())
		i += 1
B = [[0, 0, 1], [0, 1, 0], [1, 1, 0]]
C = matrix_mul(A, B)
print(C)
