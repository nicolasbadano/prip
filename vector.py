# Prip
# Vector functions

from math import sqrt, pow

def vector_add(v1, v2):
    return [v1[i] + v2[i] for i in xrange(0,len(v1))]

def vector_diff(v1, v2):
    return [v1[i] - v2[i] for i in xrange(0,len(v1))]

def vector_multiply(v, a):
    return [v[i] * a for i in xrange(0,len(v))]

def vector_norm(v):
    return sqrt(sum(pow(float(x), 2) for x in v))

def vector_normalized(v):
    norm = vector_norm(v)
    return [x / norm for x in v]

def solve_linear_2x2(A,b):
	det = determinant_2x2(A[0], A[1])
	det_x = determinant_2x2(b, A[1])
	det_y = determinant_2x2(A[0], b)
	return [det_x/det, det_y/det]

def determinant_2x2(column0, column1):
	return column0[0] * column1[1] - column0[1] * column1[0]
