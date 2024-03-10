import math
import numpy as np

node = hou.pwd()
geo = node.geometry()

points = np.array([point for point in geo.points()])

def twoPointersSearch(array: list) -> list:
    result = []
    jumpAmount = math.floor(math.sqrt(len(array)))
    i = jumpAmount
    j = 0
    
    while i < len(array):
        if array[i].attribValue("P")[1] == 0:
            break
        i+= jumpAmount
    i -= jumpAmount
    
    while j < jumpAmount and i < len(array):
        if array[i].attribValue("P")[1] == 0:
            result.append(array[i])
            
        i += 1
        j += 1
    return result
    
resultado = twoPointersSearch(points)
print(resultado)