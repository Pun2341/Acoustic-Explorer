import math
import numpy as np

threshold = 0.01
num_overtones = 40

def neighbors(center, radius):
    re = [center]
    if radius > threshold:
        for i in range(5):
            re += [[min(center[j] + (radius if i == j else 0), 1) for j in range(5)], \
                [max(center[j] - (radius if i == j else 0), 0) for j in range(5)]]
    return re

def overtones_from_vec(v):
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

    basis = np.array([ \
        [1/(n+1) for n in range(num_overtones)], \
        [1/(n+1) if n % 2 == 0 else 0 for n in range(num_overtones)], \
        [1/(n+1) if n % 3 == 0 else 0 for n in range(num_overtones)], \
        [1/(n+1) if n % 4 == 0 else 0 for n in range(num_overtones)]])
    return np.matmul(v, basis)

def neighbor_test():
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

#print(overtones_from_vec([0.5,0.5,0.5,0.5]))