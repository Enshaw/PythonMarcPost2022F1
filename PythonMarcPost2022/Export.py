import math
import time

#funtion EXPORT TO FILE
def expo2file(Outdata, nodeid, inc, outputfname, p , strid, nodeindex):
    #Output data into files
    #in order to use in matlab, '=' are not printed

    print("Output Result to file?\n[1]. .txt file\n[2]. .dat file\n[3]. Skip")
    judgeOutput = 1
    if judgeOutput == 3:
        return
    else:
        print("================================\nPrinting File %s" % outputfname)
        maxscalar = max(max(Outdata))
        print(maxscalar)
        
        minscalar = min(min(Outdata))
        print(minscalar)

        absmaxscalar = max(abs(maxscalar), abs(minscalar))
        if absmaxscalar == 0:
            e = 0
        else:
            e = int(-(math.log10(absmaxscalar)))
        #change e to in(temperarily)
        e = 0
        #outputfname = input("Output file name:")
        if judgeOutput == 1:
            outputfname=outputfname+'.txt'
        elif judgeOutput == 2:
            outputfname=outputfname+'.dat'
        
        address = "E:\\"
        fopenname = address.join(outputfname)
        fout = open(outputfname, 'w+')

        #Print node id
        print("Node id ", end = '\t', file = fout)
        for x in nodeid:
            print("%12d" % x, end = '\t', file = fout)
        print('\n', end = '', file = fout)

        #print Coordinate
        print("  X     ", end = '\t', file = fout)
        for x in nodeindex:
            print("%12.4f" % p.node(x).x, end = '\t', file = fout)
        print('\n', end = '', file = fout)
        
        print("  Y     ", end = '\t', file = fout)
        for x in nodeindex:
            print("%12.4f" % p.node(x).y, end = '\t', file = fout)
        print('\n', end = '', file = fout)
        print("  Z     ", end = '\t', file = fout)
        for x in nodeindex:
            print("%12.4f" % p.node(x).z, end = '\t', file = fout)
        print('\n', end = '', file = fout)

        for i in inc:
            print("STEP%4d" % i, end = '\t', file = fout)
            for x in Outdata[i-1]:
                t=x*(10**e)
                print("%6.6E\t" % x, end = '', file = fout)
            print('', file = fout)
        print("file %s created" % fout)
    return