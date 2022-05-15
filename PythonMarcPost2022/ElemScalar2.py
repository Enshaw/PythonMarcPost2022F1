from typing import List
import Printadd
import time
import math
import Export
import PreFunction
import Getnodeindex

#*********get scalar from every element including this node*************

class ElementIndex(list):
    def __init__(self) -> None:
        self.dic=None
        self.Nodeid=int
        self.Nodeindex=int
        self.Elementindex=[]
        self.Nodesequence=[]
        pass





#function GET ELEMENTINDEX ACCORDING TO NODE

#New module, find every element including certain node

def getELEindex(_p, _nodelist, _nodeindex):
    #get element index by node index chosen
    #input:_p: postfile; _nodelist: list of node id; _nodeindex: list of node index
    #output: 2D list: (NodeID) (Nodeindex) (elementsequence(index)[]) (sequence of node in the element[])
    nodesx = []
    nodesy = []
    nodesz = []
    for x in _nodeindex:
        nodesx.append(_p.node(x).x)
        nodesy.append(_p.node(x).y)
        nodesz.append(_p.node(x).z)
    nodesmax = [max(nodesx), max(nodesy), max(nodesz)]
    nodesmin = [min(nodesx), min(nodesy), min(nodesz)]

    ########################
    #TEST AREA
    print("NODEMAX = %10.2f\t%10.2f\t%10.2f" % (nodesmax[0], nodesmax[1], nodesmax[2]))
    print("NODEMIN = %10.2f\t%10.2f\t%10.2f" % (nodesmin[0], nodesmin[1], nodesmin[2]))
    #input("TEST06")
    ###################################

    EleChosen = []
    #EleChosen.append([])
    EleChosenIndex = []
    #EleChosenIndex.append([])
    eles = _p.elements()
    for i in range(0, eles):
        eletemp =_p.element(i)
        #get list of node ids in every element
        tempnodeids = eletemp.items
        tempnodeindexs = []
        #tempnodeindexs.append([])
        tempnodex = []
        #empnodex.append([])
        tempnodey = []
        #tempnodey.append([])
        tempnodez = []
        #tempnodez.append([])
        judgeEle = int(0)
        #get every node's index and coordinate
        jcount = 0
        for j in tempnodeids:
            tempnodeindexs.append(_p.node_sequence(j))
            tempnodex.append(_p.node(tempnodeindexs[jcount]).x)
            tempnodey.append(_p.node(tempnodeindexs[jcount]).y)
            tempnodez.append(_p.node(tempnodeindexs[jcount]).z)
            
            if (tempnodex[jcount] <= nodesmax[0]) and (tempnodex[jcount]>=nodesmin[0]):
                if (tempnodey[jcount]<=nodesmax[1]) and (tempnodey[jcount] >= nodesmin[1]):
                    if (tempnodez[jcount]<=nodesmax[2]) and (tempnodez[jcount] >=nodesmin[2]):
                        judgeEle = 1
                        
                    else:
                        pass
                else:
                    pass
            else:
                pass
            jcount = jcount+1
            if judgeEle == 1:
                EleChosen.append(eletemp)
                EleChosenIndex.append(i)
                break



        
    #get the element index of chosen element

    eleindex= []
    tempeleindex=ElementIndex()
    j = 0
    ##############################
    #TEST AREA
    #print("ElementID:")
    #for x in EleChosenIndex:
    #    print("%8d" % _p.element_id(x), end = "")
    #input("TEST05")
    ##############################
    for node in _nodelist:
        judge = 0       #judge is to judge whether the node has been found
        #eleindex.append([])

        tempeleindex.Nodeid=node #eleindex[j][0]: node id;
        tempeleindex.Nodeindex=(_nodeindex[j])   #node index

        
        tempeleindex.Elementindex=[]
        tempeleindex.Nodesequence=[]
        

        
        for i in EleChosenIndex:        #i:element index
            
            tempNlist = _p.element_scalar(i, 0)  #compare the node id with items(nodes) contained in a certain element #used to use '.item' before 08.15
            k = 0
            #circulation in element [i]
            for k in range(0,len(tempNlist)):     #x: sequence of the node in this element
                x=tempNlist[k].id
                if node == x:
                    tempeleindex.Elementindex.append(i)       #index of element
                    tempeleindex.Nodesequence.append(k)     #index of node's sequence in each element

                    k=0
                k = k+1
            if judge >= 8:  #whether 8 elements has been used
                break

        eleindex.append(ElementIndex())
        eleindex[j].Nodeid = tempeleindex.Nodeid
        eleindex[j].Nodeindex = tempeleindex.Nodeindex
        eleindex[j].Nodesequence = tempeleindex.Nodesequence
        eleindex[j].Elementindex = tempeleindex.Elementindex
        ####################################
        #TEST AREA
        if len(eleindex[j].Elementindex) == 0:
            print("ERRO in len Elementindex, node %8d" % eleindex[j].Nodeid)
            #input("TEST03")
        #####################################


        j = j+1
    #print(len(eleindex), len(eleindex[1]))


    return eleindex

def EleScalar(Inpdat, judgeI):
    #PreFunction.py is in-need for function'getnodeind'
    #JudgeI
    print("===========================================\n")
    print("====== <MODULE 3> GET ELEMENT SCALAR ======\n")
    print("===========================================\n")
    p = Inpdat.pfile
    if judgeI == 2:
        #Semi-Auto
        
        #CHOOSE SCALAR
        st1 = Inpdat.scalar
        strid = p.element_scalar_label(st1)
        print ("YOU CHOSE: ", strid)
        print("----------------------------------------------------------\n")

        #Choose node
        nodeindex = Inpdat.Nodelist

        printlen = len(nodeindex)*12
        if printlen <= 30:
            printlen = 30
        elif printlen >=80:
            printlen = 80

        for i in range(0, printlen):
            print(".", end = '')
        print('\n')
        
        
        print("  Node id  of %s" % Inpdat.Outfname)
        
        for i in range(0, printlen):
            print(".", end = '')
        print('\n')
        
        nodeid = []
        for x in nodeindex:
            nodeid.append(p.node_id(x))

        #print nodelist by nodeid
        #print("==  ", end = '')
        #for x in nodeid:
        #    print("%8d" % x, end = ' ')
        #for x in nodeid:
        #    print("============")
        #print("  ==\n")

        #get element index by nodeid
        eleIndex = getELEindex(p, nodeid, nodeindex)


        #get scalar
        print("Please set the increments contained(the postfile incudes %d increments):" % (p.increments()-1), end = '')
        
        ################################################################################################
        inc = range(1,202)
        ###################################################################################################


        scalarresult = []
        #nodeid2=[]
        #for j in range(0, len(eleIndex)):
        #    tm1=p.element_scalar(eleIndex[j][1], st1)
        #    nodeid2[j]=tm1[eleIndex[j][2]].id


        bar = Printadd.ProgressBar()
        xbar = bar(range(len(inc)))
        i=1
        for B in bar(range(len(inc))):
            p.moveto(i)
            bar.update('{0}/{1} STEP {2}.'.format(bar.curr_value, bar.max_value, bar.curr_value))
            time.sleep(0.1)
            scalarresult.append([])
            for j in range(0, len(eleIndex)):   #circulation for node id
                tsum = float(0)
                ti=[]
                eleIndextemp=eleIndex[j]
                for k in range(0,len(eleIndextemp.Elementindex)):
                    temp_eleindex=eleIndextemp.Elementindex[k]
                    temp_nodesequence=eleIndextemp.Nodesequence[k]
                    ti.append(p.element_scalar(temp_eleindex, st1)[temp_nodesequence].value)
                    tsum = tsum+ti[k]
                
                ###############
                if len(ti)==0:
                    print("IN %d Node, LEN TI = %d" % (eleIndex[j].Nodeid, len(ti)))
                    #input("TEST00")
                #############
                taverage=tsum/len(ti)

                scalarresult[i-1].append(taverage)   
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
            print("%10d" % x, end = '')
        print('\n')
  

        i = 0
        for x in nodeindex:
            print("%10.3f" % nodc[i][0],end = '')
            i = i+1
        print('\n')
        i = 0
        for x in nodeindex:
            print("%10.3f" % nodc[i][1],end = '')
            i = i+1
        print('\n')
        i = 0
        for x in nodeindex:
            print("%10.3f" % nodc[i][2],end = '')
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
        #outputfname.join(str(st1))
        Export.expo2file(scalarresult, nodeid, inc, outputfname,p, strid, nodeindex)
        
        #if (input("Work of MODULE 1 has been done, continue another work by MODULE 1?(Y/N):") == 'Y'):
        #    pass
        #else:
        #    break


        return

    elif judgeI == 1:
        judgeE =0 #judge whether the program has been run
        while True:
            print("Choose Your next option:")
            print("\n1. modify nodelist\n\n2. modify scalar option\n\n3. excecute\n")
            tswitch = PreFunction.switch(1,3,0)
            #GET NODE AND ELEMENT SEQUENCE
            if tswitch == 1:
                if judgeE == 0:
                    judgeE = 1
                elif judgeE == 2:
                    judgeE = 3
                
                #get node id by function '[list] = getnodeid(strmode, st1)'
                nodeindex = Getnodeindex.getnodeind(p)
                print("      ..............\n      .. Node id  ..\n........................\n")
                nodeid = []
                for x in nodeindex:
                    nodeid.append(p.node_id(x))
        
                #print nodelist by nodeid
                for x in nodeid:
                    print("%9d" % x, end = ' ')
                print("\n")

                #get element index by nodeid
                eleIndex = getELEindex(p, nodeid)

            #CHOOSE SCALAR
            #
            elif tswitch == 2:
                if judgeE == 0:
                    judgeE = 2
                elif judgeE == 1:
                    judgeE = 3
                #choose scalar label to be put out
                nes = p.element_scalars()
                print("Found ", nes, " element scalars:\n ")
                
                for i in range(0, nes):
                    print("%d. %s\n" % (i,p.element_scalar_label(i)))
                
                print("----------------------------------------------------------\n")
                print("Please type in the number of scalars you want to get:")
                st1 = PreFunction.switch(0,nes-1)
                strid = p.element_scalar_label(st1)
                print ("YOU CHOSE: ", strid)
                print("----------------------------------------------------------\n")

            #GET SCALAR
            #
            elif tswitch == 3:
                if not(judgeE == 3):
                    print("Input data not enough......")
                    continue
                print("Executing......")

                #get scalar
                print("Please set the increments contained(the postfile incudes %d increments):" % (p.increments()-1), end = '')
                inc = range(1,int(input()))

                scalarresult = []
                bar = Printadd.ProgressBar()
                xbar = bar(range(len(inc)))
                i=1
                for B in bar(range(len(inc))):
                    p.moveto(i)
                    bar.update('{0}/{1} STEP {2}.'.format(bar.curr_value, bar.max_value, bar.curr_value))
                    time.sleep(0.1)
                    scalarresult.append([])
                    for j in range(0, len(eleIndex)):
                        t = p.element_scalar(eleIndex[j][1], st1)[eleIndex[j][2]]
                        scalarresult[i-1].append(t.value)
                    
                    
                    i = i+1
                bar.overlay_display('Work {0} is Done.'.format(1))

                #print result
                maxscalar = max(max(scalarresult))
                minscalar = min(min(scalarresult))
                absmaxscalar = max(abs(maxscalar), abs(minscalar))
                if absmaxscalar == 0:
                    e = 0
                else:
                    e = int(-(math.log10(absmaxscalar)))
            #e=int(abs(math.log10(max(abs(max(max(scalarresult))),abs(min(min(scalarresult)))))))+1
                print("\n%s\t( x1e%d)" % (strid,-e))
                print("Node id ", end = '')
                for x in nodeid:
                    print("%10d" % x, end = '')
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
                Export.expo2file(scalarresult, nodeid, inc, Inpdat.Outputfname, p, strid, nodeindex)
                
                if (input("Work of MODULE 1 has been done, continue another work by MODULE 1?(Y/N):") == 'Y'):
                    continue
                else:
                    break

    return 1

