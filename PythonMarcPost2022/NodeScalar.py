import Export
import Printadd
import time
import math
import Print_Function

def Scalarfound(Inpdat, judgeI):
    print("===================================\n")
    print("====== <MODULE 1> GET SCALAR ======\n")
    print("===================================\n")
    

    #global JudgeI
    judgeI = 2

    if judgeI == 2:
        Scalar_found2(Inpdat)


def Scalar_found2(Inpdat, MaxInc = 0):
    #Set Increments inneed
    MaxInc = Inpdat.maxInc
    #Semi-Auto
    p = Inpdat.pfile
    #CHOOSE SCALAR
    st1 = Inpdat.scalar
    stridList = []
    print ("YOU CHOSE: ")
    i = 1
    for x in st1:
        tmpstrid = p.node_scalar_label(x)        #show the explaination of each scalar items
        print ("%d.\t%s" % (i,tmpstrid))
        stridList.append(tmpstrid)
        i = i+1

    print("----------------------------------------------------------\n")

    #Choose node　by nodes' index, translate it into node ID
    nodeindex = Inpdat.Nodelist
    print("      ..............\n      .. Node id  ..\n........................\n")
    nodeid = []
    for x in nodeindex:
        nodeid.append(p.node_id(x))

    #print nodelist by nodeid
    for x in nodeid:
        print("%9d" % x, end = ' ')
    print("\n")


    #get scalar
    #print("Please set the increments contained(the postfile incudes %d increments):" % (p.increments()-1), end = '')
    ################################################################################################
    nIncrements = p.increments()
    if MaxInc == 0 or MaxInc > nIncrements:
        MaxInc = nIncrements-1
        pass
    inc = range(1,MaxInc+2)
    ###################################################################################################

    scalarindex = []
    scalarresult = []
    bar = Printadd.ProgressBar()
    xbar = bar(range(len(inc)))
    i=1         #i is the number of current increment
    for B in bar(range(len(inc))):
        p.moveto(i)
        bar.update('{0}/{1} STEP {2}.'.format(bar.curr_value, bar.max_value, bar.curr_value))
        time.sleep(0.1)
        scalarresult.append([])
        for j in range(0, len(nodeindex)):
            for x in st1:
                t = p.node_scalar(nodeindex[j], x)
                scalarresult[i-1].append(t)
            
            
        i = i+1
    bar.overlay_display('Work {0} is Done.'.format(1))

    #get node coordinate
    nodc=[]
    i=0
    for x in nodeindex:
        nodc.append([])
        tempnode=p.node(x)
        nodc[i].append(tempnode.x)
        nodc[i].append(tempnode.y)
        nodc[i].append(tempnode.z)
        i = i+1

    scale = []
    for x in nodeindex:
        scale.append(0)
    
    Print_Function.Print_Result(scalarresult, nodeindex, stridList, scale, nodc)
    ##----------------------------------------------------
    ##print result Former
    #maxscalar = max(max(scalarresult))
    #minscalar = min(min(scalarresult))
    #absmaxscalar = max(abs(maxscalar), abs(minscalar))
    #if absmaxscalar == 0:
    #    e = 0
    #else:
    #    e = int(-(math.log10(absmaxscalar)))
        
    #print("\n%s\t( x1e%d)" % (strid,-e))
    #print("Node id ", end = '')
    #for x in nodeid:
    #    print("%8d\t" % x, end = '')
    #print('\n')

    #i = 0
    #print("\tx\t")

    ##----------------------------------------------
    ##print the coordinates of nodes
    #for x in nodeindex:
    #    print("%8f" % nodc[i][0],end = '\t')
    #    i = i+1
    #print('\n')
    #i = 0
    #print("\ty\t")
    #for x in nodeindex:
    #    print("%8f" % nodc[i][1],end = '\t')
    #    i = i+1
    #print('\n')
    #i = 0
    #print("\tz\t")
    #for x in nodeindex:
    #    print("%8f" % nodc[i][2],end = '')
    #    i = i+1
    #print('\n')
    ##---------------------------------------------

    #print('\n========', end = '')

    #for x in nodeid:
    #    print("==========", end = '')
    #print('\n')
    #for i in inc:
    #    print("STEP %3d" % i, end = '')
    #    for x in scalarresult[i-1]:
    #        t=x*(10**e)
    #        print("%10.3f" % (x*(10**e)), end = '')
    #    print('\n')
        
    #write to file
    #outputfname = Inpdat.Outfname+'-E-'+strid
    #outputfname.join(str(strid))
    #Export.expo2file(scalarresult, nodeid, inc, outputfname, p, nodeindex)
    file_format = "xlsx"
    #Export.write_to_file(Inpdat.Outfname, scalarResult, stridList, nodeindex, nodc, file_format)
    #Export.write_result_to_file(scalarresult, stridList, nodeindex, nodc, Inpdat.Outfname, Inpdat.OutDIR, file_format)
    #Export.write_scalar_to_file(scalarresult, stridList, Inpdat.Outfname, Inpdat.OutDIR, nodeid, nodc, file_format)
    #Export.write_scalar_to_file(nodeid, nodc, stridList, scalarresult, Inpdat.Outfname, Inpdat.OutDIR)
    Export.write_scalar_result_to_xlsx(scalarresult, stridList, nodeid, nodc, Inpdat.Outfname, Inpdat.OutDIR)
    Export.write_scalar_to_txt(scalarresult, stridList, nodc, nodeid, Inpdat.OutDIR, Inpdat.Outfname)
        
    #if (input("Work of MODULE 1 has been done, continue another work by MODULE 1?(Y/N):") == 'Y'):
    #    pass
    #else:
    #    break


    return