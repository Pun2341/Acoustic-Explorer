import math, random
import numpy as np

threshold = 0.15
num_overtones = 8
num_neighbors = 8 # please don't change this

def calculate_neighbors(center, radius):
    re = []
    new_center = center.copy()
    if radius > threshold: 
        for i in range(len(new_center)):
            if center[i] + radius - 1 > 0: new_center[i] -= (center[i] + radius - 1) 
            elif center[i] - radius < 0: new_center[i] -= (center[i] - radius)
        corners = [[-1,-1,-1,-1], [1,1,1,1], [1,1,-1,-1], [1,-1,1,-1], [1,-1,-1,1], [-1,1,1,-1], [-1,1,-1,1], [-1,-1,1,1]]
        for c in corners:
            re.append([new_center[i] + (radius * c[i]) for i in range(4)])
    return re
    

def calculate_intensities(v):
    depth_vector = [1/(i+1) for i in range(num_overtones)]
    even_depth_vector = [1/(i+1) if i % 2 == 0 else 0 for i in range(num_overtones)]
    reedy_vector = [0.3 if i == 6 or i == 9 else (0.4 if i == 7 or i == 8 else 0) for i in range(num_overtones)]
    matrix = np.array([depth_vector, even_depth_vector, reedy_vector])
    intensities = np.matmul(v[1:], matrix)
    intensities[0] = 1

    a = 0.001 + 0.8*v[0]
    envelope = lambda x: (x/a if x < a else (1-x)/(1-a))
    return intensities, envelope