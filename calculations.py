import math
import numpy as np

threshold = 0.01
num_overtones = 8

def neighbors(center, radius):
    re = [center]
    if radius > threshold:
        for i in range(5):
            re += [[min(center[j] + (radius if i == j else 0), 1) for j in range(5)], \
                [max(center[j] - (radius if i == j else 0), 0) for j in range(5)]]
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

    a = 0.001 + 0.8*v[0]
    envelope = lambda x: (x/a if x < a else (1-x)/(1-a))
    return intensities, envelope

if __name__ == "__main__":
    center = [0]*4
    radius = 1
    centers = neighbors(center, radius)
    while(len(centers) > 1):
        for i in range(len(centers)):
            print(str(i)+": "+str(centers[i]))
        i = int(input(": "))
        radius = radius / 2
        centers = neighbors(centers[i], radius)
    print(centers)