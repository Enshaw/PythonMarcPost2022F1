import Export
import Printadd
import time
import math

def Scalarfound(Inpdat, judgeI, MaxInc = 0):
    print("===================================\n")
    print("====== <MODULE 1> GET SCALAR ======\n")
    print("===================================\n")
    
    #Set Increments inneed
    MaxInc = Inpdat.maxInc

    #global JudgeI
    judgeI = 2

    if judgeI == 2:
        #Semi-Auto
        p = Inpdat.pfile
        #CHOOSE SCALAR
        st1 = Inpdat.scalar
        strid = p.node_scalar_label(st1)        #show the explaination of each scalar items
        print ("YOU CHOSE: ", strid)
        print("----------------------------------------------------------\n")

        #Choose node
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

        scalarresult = []
        bar = Printadd.ProgressBar()
        xbar = bar(range(len(inc)))
        i=1
        for B in bar(range(len(inc))):
            p.moveto(i)
            bar.update('{0}/{1} STEP {2}.'.format(bar.curr_value, bar.max_value, bar.curr_value))
            time.sleep(0.1)
            scalarresult.append([])
            for j in range(0, len(nodeindex)):
                t = p.node_scalar(nodeindex[j], st1)
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

        #print result
        maxscalar = max(max(scalarresult))
        minscalar = min(min(scalarresult))
        absmaxscalar = max(abs(maxscalar), abs(minscalar))
        if absmaxscalar == 0:
            e = 0
        else:
            e = int(-(math.log10(absmaxscalar)))
        
        print("\n%s\t( x1e%d)" % (strid,-e))
        print("Node id ", end = '')
        for x in nodeid:
            print("%8d\t" % x, end = '')
        print('\n')

        i = 0
        print("\tx\t")
        for x in nodeindex:
            print("%8f" % nodc[i][0],end = '\t')
            i = i+1
        print('\n')
        i = 0
        print("\ty\t")
        for x in nodeindex:
            print("%8f" % nodc[i][1],end = '\t')
            i = i+1
        print('\n')
        i = 0
        print("\tz\t")
        for x in nodeindex:
            print("%8f" % nodc[i][2],end = '')
            i = i+1
        print('\n')

        print('\n========', end = '')

        for x in nodeid:
            print("==========", end = '')
        print('\n')
        for i in inc:
            print("STEP %3d" % i, end = '')
            for x in scalarresult[i-1]:
                t=x*(10**e)
                print("%10.3f" % (x*(10**e)), end = '')
            print('\n')
        
        #write to file
        outputfname = Inpdat.Outfname+'-E-'+strid
        outputfname.join(str(strid))
        Export.expo2file(scalarresult, nodeid, inc, outputfname, p, strid, nodeindex)
        
        #if (input("Work of MODULE 1 has been done, continue another work by MODULE 1?(Y/N):") == 'Y'):
        #    pass
        #else:
        #    break


        return