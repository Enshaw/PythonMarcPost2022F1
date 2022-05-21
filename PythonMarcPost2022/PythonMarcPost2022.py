
#Updating 22.05.02: adding 'close()' in fuction 'main' during each end of a loop;

#!/usr/bin/env python
#
# chap8.py
#
# Purpose:
#   PyPost example
#   Find the max nodal scalar values
#
# Usage:
#   python chap8.py
#
# Dependencies
#   Uses PyPost methods:
#     node_scalars
#     node_scalar_labels
#     moveto
#   sys is needed
#   Post file 

#GLOBAL: tcon(whether need to be confirmed)
#

from py_post import *
import sys
import math
import time
import Printadd

import ElemScalar2
import NodeScalar
import Export
#Print Progressbar in the command window
from Printadd import*

import PreFunction
import Getnodeindex


tcon = 0
#global judgeI = None









#function CONFIRMINPUT
def confirminput(temp):
    #fucthon to make confirmation(......(Y/N):)
    #if typein Y(Capital), retrun the value input before, otherwise return 0
    print("You chose:%s; Please make your confirmation(Y/N)\n" % (temp))
    strtemp = input()
    if (strtemp == 'Y'):
        return temp
    else:
        return 0

def Vectorfound(p, judgeI):
    #PreFunction.py is in-need(for fuction 'getnodeind' to get node index)
    print("=========================\n")
    print("= <MODULE 2> GET VECTOR =\n")
    print("=========================\n")
    
    judgeE =0 #judge whether the program has been run
    while True:
        print("Choose Your next option:")
        print("1. modify nodelist\n2. modify vector option\n3. excecute")
        tswitch = PreFunction.switch(1,3,0)
        #GET NODE
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

        #CHOOSE VECTOR TYPE
        elif tswitch == 2:
            if judgeE == 0:
                judgeE = 2
            elif judgeE == 1:
                judgeE = 3
            #choose vecto label to be put out
            nns = p.node_vectors()
            print("Found ", nns, " node vectors:\n ")
            
            for i in range(0, nns):
                print("%d. %s\n" % (i,p.node_vector_label(i)))
            
            print("----------------------------------------------------------\n")
            print("Please type in the number of vectors you want to get:")
            st1 = PreFunction.switch(0,nns-1)
            strid = p.node_vector_label(st1)
            print ("YOU CHOSE: ", strid)
            print("----------------------------------------------------------\n")


        elif tswitch == 3:
            if not(judgeE == 3):
                print("Input data not enough......")
                continue
            print("Executing......")

            #get vector
            print("Please set the increments contained(the postfile incudes %d increments):" % (p.increments()-1), end = '')
            inc = range(1,int(input()))

            vectorresult = []
            bar = ProgressBar()
            xbar = bar(range(len(inc)))
            i=1
            for B in bar(range(len(inc))):
                p.moveto(i)
                #print("%d step" % i, end ='')
                bar.update('{0}/{1} STEP {2}.'.format(bar.curr_value, bar.max_value, bar.curr_value))
                time.sleep(0.1)
                vectorresult.append([])
                for x in nodeindex:
                    t = p.node_vector(x, st1)
                    vectorresult[i-1].append(t)           
                i = i+1
            bar.overlay_display('Work {0} is Done.'.format(1))

            #print result
            maxvector = max(max(vectorresult))
            minvector = min(min(vectorresult))
            absmaxvector = max(abs(maxvector), abs(minvector))
            if absmaxvector == 0:
                e = 0
            else:
                e = int(abs(math.log10(absmaxvector)))
           #e=int(abs(math.log10(max(abs(max(max(vectorresult))),abs(min(min(vectorresult)))))))+1
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
                for x in vectorresult[i-1]:
                    t=x*(10**e)
                    print("%10.3f" % (x*(10**e)), end = '')
                print('\n')
            
            #write to file
            print("Output Result to file?\n[1]. .txt file\n[2]. .dat file\n[3]. Skip")
            judgeOutput = PreFunction.switch(1,3,0)
            if judgeOutput == 3:
                pass
            else:
                outputfname = input("Output file name:")
                if judgeOutput == 1:
                    outputfname.join('.txt')
                elif judgeOutput == 2:
                    outputfname.join('.dat')
                fout = open(outputfname, 'w+')
                print("TITLE\t%s" % p.title(), file = fout)
                print("\n%s\t( x1e%d)" % (strid,-e), file = fout)
                print("Node id ", end = '', file = fout)
                for x in nodeid:
                    print("%10d" % x, end = '', file = fout)
                print('\n========', end = '', file = fout)

                for x in nodeid:
                    print("==========", end = '', file = fout) 
                print('\n', file = fout)
                for i in inc:
                    print("STEP %3d" % i, end = '', file = fout)
                    for x in vectorresult[i-1]:
                        t=x*(10**e)
                        print("%10f" % (x*(10**e)), end = '', file = fout)
                    print('\n', file = fout)
            
            if (input("Work of MODULE 1 has been done, continue another work by MODULE 1?(Y/N):") == 'Y'):
                continue
            else:
                break
    return 1
    




def main():
    global judgeI
    
    #need confirmmation?
    print("****************************************\nRun this program without being confirmed?(Y/N):", end = '')
    global tcon
    #if input() == 'Y':
    #    tcon = 0
    #else:
    tcon = 0
    
    
    print("\n")
    for i in range(1,40):   
        
        print("*", end = '')
        time.sleep(0.01)
    print('\n')

    #Choose the TYPE of Output-Data that you Expected(NODE-VECTOR/NODE-SCALAR\ELEMENT SCALAR\)
    print("PLEASE CHOOSE THE WORKING MODULE:\n1. NODE SCALAR\n\n2. NODE VECTOR\n\n3. ELEMENT SCALAR\n\n4. QUIT\n")
    
    stmod=PreFunction.switch(1,4,0)            ############
    if stmod == 4:
        return 0
    
    #typein filename and check if file is accessable
    #CHOOSE INPUT MODE
    print("****************************************\nChoose input mode\n1. Manual\n2. Semi-Auto\n3. From File")
    judgeI = int(input())
    print("Input Mode = %d" % judgeI)
    
    Inpdat = PreFunction.preex(stmod, judgeI)    #Inpdat:Class Inputdata from PreFunction.py'
                                    #Including: fname/ Outputfname/ pfile/ Scalar/ Nodelist/ stmod
    if Inpdat == 0:
        print('\n==============================\nProcess Shut Down\n==============================')
        return 0

    #stmod = Inpdat[0].stmod         #Parameter stmod:TYPE of Output-Data that you Expected(NODE-VECTOR/NODE-SCALAR\ELEMENT SCALAR\)

    icircle = 0
    while 1:#infinite cycling

 
        #Execute    
        stmod = Inpdat[icircle].stmod  #Parameter stmod:TYPE of Output-Data that you Expected(NODE-VECTOR/NODE-SCALAR\ELEMENT SCALAR\)
    
        #excute selected mode
        if(stmod == 4):
            print("PROGRAM SHUTDOWN. PRESS ENTER TO CONTINUE...\n")
            input()
            return 0
        elif (stmod == 1):
            NodeScalar.Scalarfound(Inpdat[icircle], judgeI)
        elif (stmod == 2):
            Vectorfound(Inpdat[icircle], judgeI)
        elif (stmod == 3):
            ElemScalar2.EleScalar(Inpdat[icircle], judgeI)
        
        else:
            pass
        

        ####################################
        # close file
        Inpdat[icircle].pfile.close()

        icircle = icircle + 1
        if icircle >= len(Inpdat):
            if input("WORK IS DONE, QUIT PROGRAM?(Y/N):") == 'Y':
                return 1
            else:
                break
        else:
            pass

    
    return 1



if __name__ == '__main__':
    while True:
        j1=main()
        if input("RUN Again?(Y/N):") == 'Y':
            continue
        else:
            break
    print("[Tips: When Quiting The Program, type 'QUIT' to quit the python program]\n=================================================\n")


#"E:\WORKFOLDER\FrameExp\FEM\IEP\F25-30-0-IEP0413_job1.t16"
#E:\FEM\Frame\IEP\F40-37-50-IEP_job1.t16