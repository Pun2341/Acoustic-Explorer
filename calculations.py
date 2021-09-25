import math

threshold = 0.01
num_overtones = 20

def neighbors(center, radius):
    re = [center]
    if radius > threshold:
        for i in range(5):
            re += [[min(center[j] + (radius if i == j else 0), 1) for j in range(5)], \
                [max(center[j] - (radius if i == j else 0), 0) for j in range(5)]]
    return re

def overtones_from_vec(v):
    v = [e*2 - 1 for e in v]
    re = []
    for n in range(1, num_overtones):
        x = 1 - 2*math.exp(-n/2)
        y = v[0]
        y += v[1] * (x+1)/2
        y += v[2] * (0.5*(3*x*x + 1) + 1)/2
        y += v[3] * (0.5*(5*x*x*x - 3*x) + 1)/2
        re.append(y)
    return re

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