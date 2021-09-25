import math

threshold = 0.01
num_overtones = 6

def neighbors(center, radius):
    re = [center]
    if radius > threshold:
        for i in range(5):
            re += [[min(center[j] + (radius if i == j else 0), 1) for j in range(5)], \
                [max(center[j] - (radius if i == j else 0), 0) for j in range(5)]]
    return re

def overtones(v):
    v = [e*2 - 1 for e in v]
    re = []
    for n in range(1, num_overtones):
        x = 1 - 2*math.exp(-n/2)
        y = v[0]
        y += v[1] * x
        y += 0.5*(3*x*x + 1)
        y += 0.5*(5*x*x*x - 3*x)
        re.append(y)
    return re

def neighbor_test():
    center = [0]*5
    radius = 1
    centers = neighbors(center, radius)
    while(len(centers) > 1):
        for i in range(len(centers)):
            print(str(i)+": "+str(centers[i]))
        i = int(input(": "))
        radius = radius / 2
        centers = neighbors(centers[i], radius)
    print(centers)