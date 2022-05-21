import math
import time

#funtion EXPORT TO FILE
def expo2file(Outdata, nodeid, inc, outputfname, p , nodeindex):
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



import os
import openpyxl

def write_scalar_result_to_xlsx(ScalarResult, ScalarNameList, NodeIndex, nodc, OutputFname, OutDIR):
    # Get the number of increments and scalar types
    num_increments = len(ScalarResult)
    num_scalar_types = len(ScalarResult[0]) // len(NodeIndex)

    # Check if OutDIR exists, if not, create it
    if not os.path.exists(OutDIR):
        os.makedirs(OutDIR)
        
    # Create the workbook
    workbook = openpyxl.Workbook()

    # Write the scalar results to different worksheets
    for i in range(num_scalar_types):
        # Create the worksheet
        worksheet = workbook.create_sheet(title=ScalarNameList[i])
        
        # Write the header: NodeIndex, x, y, z, ScalarResult for each increment
        worksheet.append(['NodeIndex'] + ['x', 'y', 'z'] + [f'Increment {j+1}' for j in range(num_increments)])
        
        # Write the node index, x, y, z and scalar result for each node
        for j in range(len(NodeIndex)):
            node_index = NodeIndex[j]
            node_x, node_y, node_z = nodc[j]
            scalar_results = [ScalarResult[k][j * num_scalar_types + i] for k in range(num_increments)]
            worksheet.append([node_index, node_x, node_y, node_z] + scalar_results)
    
    # Save the workbook to a file
    file_path = os.path.join(OutDIR, OutputFname + '.xlsx')
    workbook.save(file_path)


def write_scalar_to_txt(ScalarResult, ScalarNameList, nodc, nodeid, OutDIR, OutputFname):
    def scientific_notation(num, decimal_places=2):
        return '{:.{}E}'.format(num, decimal_places)

    n = len(ScalarResult)
    m = len(ScalarNameList)
    b = len(nodeid)
    
    if not os.path.exists(OutDIR):
        os.makedirs(OutDIR)
    
    for i in range(len(ScalarNameList)):
        file_path = os.path.join(OutDIR, OutputFname + '-' + ScalarNameList[i] + '.txt')
        with open(file_path, 'w') as f:
            print('Scalar Name:', ScalarNameList[i], file=f)
            print('{:<8}'.format('Inc.'), end='', file=f)
            for j in range(b):
                print('{:<15}'.format(nodeid[j]), end='', file=f)
            print('', file=f)
            print('{:<8}'.format('x'), end='', file=f)
            for j in range(b):
                print('{:<15}'.format(scientific_notation(nodc[j][0])), end='', file=f)
            print('', file=f)
            print('{:<8}'.format('y'), end='', file=f)
            for j in range(b):
                print('{:<15}'.format(scientific_notation(nodc[j][1])), end='', file = f)
            print('', file=f)
            print('{:<8}'.format('z'), end='', file=f)
            for j in range(b):
                print('{:<15}'.format(scientific_notation(nodc[j][2])), end='', file=f)
            print('', file=f)
            for k in range(n):
                print('{:<8}'.format(k+1), end='', file=f)
                for j in range(b):
                    idx = (i*b)+j
                    value = ScalarResult[k][idx]
                    print('{:<15}'.format(scientific_notation(value)), end='', file=f)
                print('', file=f)
            print('', file=f)