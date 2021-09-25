import math, random
import numpy as np

threshold = 0.15
num_overtones = 8
num_neighbors = 8 # please don't change this

def calculate_neighbors(center, radius):
    # re = [center]
    # if radius > threshold:
    #     for i in range(4):
    #         re += [[min(center[j] + (radius if i == j else 0), 1) for j in range(4)], \
    #             [max(center[j] - (radius if i == j else 0), 0) for j in range(4)]]
    # return re

    re = []
    new_center = center.copy()
    if radius > threshold: 
        for i in range(len(new_center)):
            if center[i] + radius - 1 > 0: new_center[i] -= (center[i] + radius - 1) 
            elif center[i] - radius < 0: new_center[i] -= (center[i] - radius)
        #for _ in range(num_neighbors):
            #re.append([c+random.random() * radius for c in new_center])
        corners = [[-1,-1,-1,-1], [1,1,1,1], [1,1,-1,-1], [1,-1,1,-1], [1,-1,-1,1], [-1,1,1,-1], [-1,1,-1,1], [-1,-1,1,1]]
        for c in corners:
            re.append([new_center[i] + (radius * c[i]) for i in range(4)])
    return re
    

def calculate_intensities(v):
    #v = [e*2 - 1 for e in v]
    #re = []
    #for n in range(1, num_overtones):
        # x = 1 - 2*math.exp(-n/2)
        # y = v[0]
        # y += v[1] * (x+1)/2
        # y += v[2] * (0.5*(3*x*x + 1) + 1)/2
        # y += v[3] * (0.5*(5*x*x*x - 3*x) + 1)/2
        # re.append(y)
    #return re

    # basis = np.array([ \
    #     [1/(n+1) for n in range(num_overtones)], \
    #     [1/(n+1) if n % 2 == 0 else 0 for n in range(num_overtones)], \
    #     [1/(n+1) if n % 3 == 0 else 0 for n in range(num_overtones)], \
    #     [1/(n+1) if n % 4 == 0 else 0 for n in range(num_overtones)]])
    # return np.matmul(v, basis)

    depth_vector = [1/(i+1) for i in range(num_overtones)]
    even_depth_vector = [1/(i+1) if i % 2 == 0 else 0 for i in range(num_overtones)]
    reedy_vector = [0.3 if i == 6 or i == 9 else (0.4 if i == 7 or i == 8 else 0) for i in range(num_overtones)]
    matrix = np.array([depth_vector, even_depth_vector, reedy_vector])
    intensities = np.matmul(v[1:], matrix)
    intensities[0] = 1

    a = 0.001 + 0.8*v[0]
    envelope = lambda x: (x/a if x < a else (1-x)/(1-a))
    return intensities, envelope

if __name__ == "__main__":
    center = [0]*4
    radius = 0.5
    centers = calculate_neighbors(center, radius)
    while(len(centers) > 1):
        for i in range(len(centers)):
            print(str(i)+": "+str(centers[i]))
        i = int(input(": "))
        radius = radius / 2
        centers = calculate_neighbors(centers[i], radius)
    print(centers)
