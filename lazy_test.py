import numpy as np
from lazy import *

N = 8096
print("Step 1")
def createMatrix(n):
	return np.random.randn(n,n)

def mm(a,b):
	return force(a) @ force(b)

print("Step 2")
m1 = lazy(createMatrix(N))
print("Step 3")
m2 = lazy(createMatrix(N))
print("Step 4")
print("Step 1")
print("Step 1")
print("Step 1")
print("Step 1")
print("Step 1")
print("Step 1")

c = lazy(mm,m1,m2)
print("Step 5")
print("Step 6")
print("Step 7")
print("Step 8")

print(c)