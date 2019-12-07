def langford_data_structure(N):
    # n1,n2,... means that the value has been used
    # p1,p2,... means that the position has been used
    def value(i):
        return sys.intern('n%d' % (i,))

    def position(i):
        return sys.intern('p%d' % (i,))

    X = set([value(i) for i in range(1, N+1)] +
            [position(i) for i in range(2*N)])

    Y = {}

    for n in range(1, N+1): # Para cada valor de 1 a N
        for p in range(2*N-n-1):
            Y[value(n)+position(p)] = [value(n), position(p), position(p+(n+1))]    

    X = {j: set() for j in X}
    for i in Y:
        for j in Y[i]:
            X[j].add(i)

    return X, Y