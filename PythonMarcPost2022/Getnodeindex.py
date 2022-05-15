#upgrade in 2022/5/8: getnodeind mode1 _PreviousData.Nodedata = int(x) (former: =i)
#upgrade in 2022/5/14: getnodeind and getnodeindrepeat: mode1 node.x/y/z == cordinatelist[x][1/2/3] → abs(node.x/y/z-cordinatelist[x][1/2/3])<=1e-5
#upgrade in 2022/5/15: getnodeind and getnodeindrepeat: mode2 for x in range(0, coordinlist) changed to coordinlist-1

import PreFunction

class Modedata(list):
    def __init__ (self):
        self.mode=int()
        self.Nodedata=list()  #node index
        self.Coordinatedata=list()
        self.CoordinateRange = list()

#Read in data as matrix from txt file
def loadDatadet (infile, k):
    f = open(infile, 'r')
    sourceInLine = f.readlines()
    dataset = []
    for line in sourceInLine:
        temp1 = line.strip('\n')
        temp2 = temp1.split('\t')
        dataset.append(temp2)
    for i in range(0, len(dataset)):
        for j in range(k):
            dataset[i].append(float(dataset[i][j]))
        del(dataset[i][0:k])
    return dataset
        
#   Get Node_id duing the 1st loop
def getnodeind(fp):
    #get the nodeid by mode 'findmode', from file 'fp'
    #findmode:(
    # Mode 1 (according to node id manually typed in);
    # Mode 2 (according to x, y, z cordinate);
    # Mode 3 (according to restriction to x, y, z cordinates[xmin, xmax] [ymin ymax] [zmin zmax])
    # Mode 4 (according to set id)(under development!!!)
    # Mode 5 (according to x, y, z cordinate(individual), from file;)
    #in vision beta1, mode3 cannot be used
    
    #######################################
    print("GET NODE ELEMENT ID")
    
    ###############################################
    nnodeT = fp.nodes()
    listid = []
    listNodeid = []
    #set mode
    print("Input the nodes' id by:\n1. MANUAL(by node_id)\n\n2. MANUAL(by coordinate)\n\n3. SELECTION(by coordinate)\n\n4. SELECTION(by sets-UNABLE)\n\n5. From File(by coordinate)\n\n6. QUIT\n")
    findmode = PreFunction.switch(1,3,0)
    _PreviousData=Modedata()
    #Mode1(By Node_id)
    if (findmode == 1):
        _PreviousData.mode = 1
        print("------------\nGET NODE MODE 1\n------------\nPlease typein the node id:")
        while True:

            tempstr = input().split('\t')
            for x in tempstr:
                for i in range (1,nnodeT):
                    if fp.node(i).id == int(x):
                        listid.append(i)
                        listNodeid.append(int(x)) #rectified in may,8
        
            judge=input("continue to input?(Y/N):")
            if (judge) == 'N':
                break
        _PreviousData.Nodedata = listNodeid     #rectified in may,8
        
    
    #Mode2(By Coordinates)
    
    elif (findmode == 2):
        _PreviousData.mode = 2
        print("------------\nGET NODE MODE 2\n------------\nPlease typein the Coordinates(x y z by lines, end the input by typing \"Enter\"):")
        Coordinlist = []
        i = 0
        while True:
            tempc = input()
            if tempc == "s" or tempc == '':
                print("END\n")
                break
            else:
                Coordinlist.append([])
                for x in tempc.split():
                    Coordinlist[i].append(float(x))
                
                i = i+1


        for x in range(0, len(Coordinlist)-1):
            for k in range(1, nnodeT):
                nod = fp.node(k)
                if abs((nod.x) - Coordinlist[x][0])<=1e-5 and abs((nod.y) - Coordinlist[x][1])<=1e-5 and abs((nod.z) - Coordinlist[x][2])<=1e-5:
                    listid.append(k)
                    print(".", end = '')
                else:
                    pass
        _PreviousData.Coordinatedata = Coordinlist

  
    #Mode3(By Coordinate range)
    elif (findmode == 3):
        _PreviousData.mode = 3
        for i in range(0, 120):
            print('-', end ='')
        print('\n')
        for i in range(0, 50):
            print('-', end ='')
        print("  GET NODE MODE 3   ", end = '')
        for i in range(0, 50):
            print('-', end ='')
        print('\n')
        for i in range(0, 120):
            print('-', end = '')
        print('\n')
        print("\nPlease typein the Rage of Coordinate:")
        XRANGE = []
        YRANGE = []
        ZRANGE = []
        i=1
        #if i>2 stop
        for x in input("X Range:(lowerlimit upperlimit):").split():
            XRANGE.append(float(x))
            i=i+1
            if i>2:
                break
        i=1
        #if i>2 stop
        for x in input("Y Range:(lowerlimit upperlimit):").split():
            YRANGE.append(float(x))
            i=i+1
            if i>2:
                break
        i=1
        #if i>2 stop
        for x in input("Z Range:(lowerlimit upperlimit):").split():
            ZRANGE.append(float(x))
            i=i+1
            if i>2:
                break
        #find nodes according to the condition
        
        for k in range(1,nnodeT):
            nod = fp.node(k)
            if (nod.x<=XRANGE[1] and nod.x>=XRANGE[0]) and (nod.y<=YRANGE[1] and nod.y>=YRANGE[0]) and (nod.z<=ZRANGE[1] and nod.z>=ZRANGE[0]):
                listid.append(k)
                print(".", end = '')
            else:
                pass
        _PreviousData.CoordinateRange.append(XRANGE)
        _PreviousData.CoordinateRange.append(YRANGE)
        _PreviousData.CoordinateRange.append(ZRANGE)

    #Mode4(By Sets)
    elif (findmode == 4):
        print("------------\nGET NODE MODE 4\n------------\nPlease typein the SET id:")

    #Mode5(From file by coordinates)
    elif (findmode == 5):
        _PreviousData.mode = 5
        print("------------\nGET NODE MODE 5\n------------\nPlease typein the path of File containing Coordinates:\n\nFormat:\nx[tab] y[tab] z\n...\n\n(end the input by typing \"Enter\"):")
        nodelistfile = input()
        Coordinlist = loadDatadet(nodelistfile, 3)

        for x in range(0, len(Coordinlist)):
            for k in range(1, nnodeT):
                nod = fp.node(k)
                if (nod.x) == Coordinlist[x][0] and (nod.y) == Coordinlist[x][1] and (nod.z) == Coordinlist[x][2]:
                    listid.append(k)
                    print(".", end = '')
                else:
                    pass
        _PreviousData.Coordinatedata = Coordinlist

    #print("Node_id input:")
    #for x in listid:
    #    print("%9d" % x, end = ' ')
    #print("\n")
    for i in range(0, 120):
        print('.', end = '')
    print('\n')
    for i in range(0, 50):
        print('.', end = '')
    print("  Input Finished   ", end = '')
    for i in range(0, 50):
        print('.', end = '')
    print('\n')
    for i in range(0, 120):
        print('.', end = '')
    print('\n')

    i=0
    for x in listid:
        print("%8d" % fp.node_id(x), end = '')
        i=i+1
        if i % 15 == 0:
            print('\n')
    print('\n')
    for i in range(0, 120):
        print('.', end = '')
    print('\n')
    return [listid, _PreviousData]



#   Get Node_id during the 2nd loop and afterwards
def getnodeindrepeat(fp, _PreviousData):
    #get the nodeid in mode 'findmode', from file 'fp'
    #findmode(1(according to node id manually typed in),2(according to restriction to the x, y, z coordinate) or 3(according to set id) )
    #in vision beta1, mode3 cannot be used

    #repeat mode selection:(Mode dic.) (Nodelistdata （mode1）) (Coordinatedata(mode 2)) (CoordinateRange (mode3))
    
    #set mode
    nnodeT = fp.nodes()
    findmode = _PreviousData.mode
    listNodeid = []
    listid = []
    #Mode1
    if (findmode == 1):
        print("------------\nGET NODE MODE 1\n------------\n")
        listNodeid = _PreviousData.Nodedata
        for x in listNodeid:
            for i in range(1, nnodeT):
                if fp.node(i).id == x:
                    listid.append(i)
                    #rectified in may,8
                    break


        
    
    #Mode2(By Coordinates)
    elif (findmode == 2):
        listid = []
        print("------------\nGET NODE MODE 2\n------------\nPlease typein the Coordinates(x y z by lines, end the input by typing \"Enter\"):")
        Coordinlist = _PreviousData.Coordinatedata


        for x in range(0, len(Coordinlist)-1):
            for k in range(1, nnodeT):
                nod = fp.node(k)
                if abs((nod.x) - Coordinlist[x][0])<=1e-5 and abs((nod.y) == Coordinlist[x][1])<=1e-5 and abs((nod.z) == Coordinlist[x][2])<=1e-5:
                    listid.append(k)
                    print(".", end = '')
                else:
                    pass

    
    
    #Mode3(By Coordinate range)
    elif (findmode == 3):
        listid = []
        for i in range(0, 120):
            print('-', end ='')
        print('\n')
        for i in range(0, 50):
            print('-', end ='')
        print("  GET NODE MODE 3   ", end = '')
        for i in range(0, 50):
            print('-', end ='')
        print('\n')
        for i in range(0, 120):
            print('-', end = '')
        print('\n')
        print("\nPlease typein the Rage of Coordinate:")
        XRANGE = _PreviousData.CoordinateRange[0]
        YRANGE = _PreviousData.CoordinateRange[1]
        ZRANGE = _PreviousData.CoordinateRange[2]
        #############################
        #TEST AREA
        print("X Range:%6.2f\t%.2f" % (XRANGE[0], XRANGE[1]))
        print("Y Range:%6.2f\t%.2f" % (YRANGE[0], YRANGE[1]))
        print("Z Range:%6.2f\t%.2f" % (ZRANGE[0], ZRANGE[1]))
        #input("TEST02")
        ############################
        
        for k in range(1,nnodeT):
            nod = fp.node(k)
            if (nod.x<=XRANGE[1] and nod.x>=XRANGE[0]) and (nod.y<=YRANGE[1] and nod.y>=YRANGE[0]) and (nod.z<=ZRANGE[1] and nod.z>=ZRANGE[0]):
                listid.append(k)
                print(".", end = '')
            else:
                pass

    #Mode4(By Sets)
    elif (findmode == 4):
        print("------------\nGET NODE MODE 4\n------------\nPlease typein the SET id:")

    #Mode5(From File By Coordinates)
    elif (findmode == 5):
        listid = []
        print("------------\nGET NODE MODE 2\n------------\nPlease typein the Coordinates(x y z by lines, end the input by typing \"Enter\"):")
        Coordinlist = _PreviousData.Coordinatedata


        for x in range(0, len(Coordinlist)):
            for k in range(1, nnodeT):
                nod = fp.node(k)
                if (nod.x) == Coordinlist[x][0] and (nod.y) == Coordinlist[x][1] and (nod.z) == Coordinlist[x][2]:
                    listid.append(k)
                    print(".", end = '')
                else:
                    pass

    #print("Node_id input:")
    #for x in listid:
    #    print("%9d" % x, end = ' ')
    #print("\n")
    for i in range(0, 120):
        print('.', end = '')
    print('\n')
    for i in range(0, 50):
        print('.', end = '')
    print("  Input Finished   ", end = '')
    for i in range(0, 50):
        print('.', end = '')
    print('\n')
    for i in range(0, 120):
        print('.', end = '')
    print('\n')

    i=0
    for x in listid:
        print("%8d" % fp.node_id(x), end = '')
        i=i+1
        if i % 15 == 0:
            print('\n')
    print('\n')
    for i in range(0, 120):
        print('.', end = '')
    print('\n')
    return listid