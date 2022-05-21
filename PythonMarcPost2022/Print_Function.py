def Print_Result(ScalarResult, NodeIndex, ScalarNameList, Scale, nodc):
    def scientific_notation(num, decimal_places=2):
        return '{:.{}E}'.format(num, decimal_places)
    
    n = len(ScalarResult)
    m = len(ScalarNameList)
    b = len(NodeIndex)
    
    for i in range(m):
        print('Scalar Name:', ScalarNameList[i])
        print('Scale: x10^-{}'.format(Scale[i]))
        print('{:<8}'.format('Inc.'), end='')
        for j in range(b):
            print('{:<15}'.format(NodeIndex[j]), end='')
        print()
        print('{:<8}'.format('x'), end='')
        for j in range(b):
            print('{:<15}'.format(scientific_notation(nodc[j][0])), end='')
        print()
        print('{:<8}'.format('y'), end='')
        for j in range(b):
            print('{:<15}'.format(scientific_notation(nodc[j][1])), end='')
        print()
        print('{:<8}'.format('z'), end='')
        for j in range(b):
            print('{:<15}'.format(scientific_notation(nodc[j][2])), end='')
        print()
        for k in range(n):
            print('{:<8}'.format(k+1), end='')
            for j in range(b):
                idx = (i*b)+j
                value = ScalarResult[k][idx]/10**Scale[i]
                print('{:<15}'.format(scientific_notation(value)), end='')
            print()
        print()