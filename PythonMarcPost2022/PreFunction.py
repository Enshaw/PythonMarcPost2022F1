#Class to store the filename, scalar item and nodelist for each working circle
#Updates(22.05.02):
#   1. completed the read_in_method3 (fromfile) in fuction input_fname(judgeI);
#Updates (22.05.16) add folder 'result\' to output routine
#Updates (22.05.17) rectified the problem caused by the former update 0516
import Getnodeindex
from py_post import *
import datetime

#function CONFIRMINPUT


def input_MaxInc(size):
    #this function is for getting the number of increments needed in every postfile from keyboard.
    
    MaxInc = [0] * size
    for i in range(size):
        data = input(f"Enter the value of MaxInc[{i}]: ")
        if data.upper() == 'D' or data.lower() == 'default':
            MaxInc = [0] * size
            break
        elif len(data) > 1 and (data[-1].upper() == 'Y' or data[-1].upper() == 'Y'):
            try:
                value = int(data[:-1])
                MaxInc = [value] * size
                break
            except:
                print("Invalid input. Please enter a valid number or 'D/default'.")
                continue
        else:
            try:
                MaxInc[i] = int(data)
            except:
                print("Invalid input. Please enter a valid number or 'D/default'.")
                continue
    return MaxInc


def confirminput(temp):
    #fucthon to make confirmation(......(Y/N):)
    #if typein Y(Capital), retrun the value input before, otherwise return 0
    print("You chose:%s; Please make your confirmation(Y/N)\n" % (temp))
    strtemp = input()
    if (strtemp == 'Y'):
        return temp
    else:
        return 0


def switch(rangeinp1, rangeinp2, _tcon):
    #function CHOOSE.SWITCH
    judge = 1
    while True:
        if judge == 0:
            print("reinput:", end = '')
        inptemp = int(input())
        if not (inptemp>=rangeinp1 and inptemp<=rangeinp2):
            print("Input Erro. Please retype:", end = ' ')
            continue

        _tcon
        print("tcon %d" % _tcon)
        if _tcon == 1:
            judge = confirminput(inptemp)
            if judge == 0:
                continue
            else:
                break
        else:
            break
    return inptemp


class Inputdata(list):
    def __init__(self):
        #Initiations
        self.dic = None
        self.fname = ''     #marc post file name
        self.scalar = list  #types of scalars for output
        self.stmod = int
        self.Nodelist = []
        self.Outfname = ""
        self.OutDIR = ""
        #pfile:variaty to store the '.t16' postfile from Marc
        self.pfile = None  
        self.additionalarry = None

    
    
    def addfile(self,fname, _OutDIR):
        #Function 'addfile':open Marc's Post file as variable 'pfile', also give the output filename and adress.
        self.pfile = post_open(fname)
        #Find the part including filename(.t16) in the list of strings(list:filenamelist)
        tempstrlist = fname.split('\\')
        tempstr = tempstrlist[len(tempstrlist)-1]
        
        OutFname = (tempstr[0:tempstr.find(".t16")])  #-1 is deleted
        self.Outfname = OutFname 
        self.OutDIR = _OutDIR
        self.fname=OutFname;    #changed due to the change in upper 3 lines
        print("Postfile Imported.")
        #To test if the post-file is opened successfully or, it is either a vacant file or being opened with erros
        try:
            self.pfile.moveto(1)
            return 1    
        except:
            print("Error opening post file:%s. Postfile not accessable.\n" % fname)
            print("Program shutdown when open \"%s\".........." % fname)
            return 0
       

def input_fname(judgeI):
    #get a list of filenameS calld '_filenamelist[i]'(string x N)
    
    _filenamelist = []
    if judgeI == 3:
        # for Mode 3(from file):
        # format of the filename_list file should including adaptable adress(absolute or relative file path\filename)
        print("\nPlease type in the filename including adress of Postfiles\nFormat:\npath/fname\npat/fname\n...\nLISTFILE:")
        listfile_name = input()
        f_filelist = open(listfile_name)
        lines = f_filelist.readlines()
        for line in lines:
            _filenamelist.append(line)
        f_filelist.close
        
    else:
        # for Mode 1(manual) and Mode 2(semi-auto):
        #     
        print("\nPlease input the filename list(End with 'ENTER')")
        #Input filename(if choosing mode1, then break when the 1st filename is inputed)
        while True:
            tempc = input()
            if tempc == '' or tempc == '\n':
                break
            _filenamelist.append(tempc)
            if judgeI == 1:
                break

    #Output Filename
    print("\nOutput file shares the same title with the post file.")
    return(_filenamelist)

def read_in(_filenamelist, _LEN, _OutDIR = "result/"):
    #
    # Input： 
    # _filenamelist: list of strings of postfile names;
    # _LEN: the length(rows) of _filenamelist;
    #
    # Output:
    # INP0: list of objects (belong to class "Inputdata")
    #
    # Dependence:
    #   class: Inputdata;
    #   Function from this file: NONE;
    #   Function from other files: Getnodeindex.getnodeind()

    print("\n==============================\n!!***** ******* read  in file  !!\n==============================\n")

    # _judgeInpN:   judge whether the nodes in different importing loops are the same; 
    #               while during the first loop, it's set to be '0';
    _judgeInpN = 0       #initiation. judgeInpN is for judging whether the node to be readed-in afterward will using the same strategy/the same index
    #create the filelist '_INP0'
    _INP0 = list()

    for i in range(0, _LEN):
        ###########FOR TEST
        #print("ROUND %d (LEN = %d)" % (i, _LEN))
        #input()
        ###########
        _tempNode = []
        _tempinp = Inputdata()
        print(_filenamelist[i], end = '\n\n')
        #read-in files and add to object 'tempinp', with item 'pfile','fname' and 'Outputfname'
        print("Reading Files %s......" % _filenamelist[i])
        _pp=_tempinp.addfile(_filenamelist[i], _OutDIR)
        if _pp == 0:
            print("\n==============================\n!!Erros occured while importing!!\n==============================\n")
            return 0
        #print("pp %d" % i)
        ###################
        #print("JUDGEN == %d" % _judgeInpN)
        #################
        if _judgeInpN == 0 or _judgeInpN == 1:
            #################
            print("GETONDE INIT.......")
            #################
            [_tempNode, InputData] = Getnodeindex.getnodeind(_tempinp.pfile)    #InputData:value '_PreviousData' in function

        elif _judgeInpN == 2:
            #################
            print("GETONDE REPEAT.......")
            #################
            _tempNode = Getnodeindex.getnodeindrepeat(_tempinp.pfile, InputData)



        for xx in _tempNode:
            _tempinp.Nodelist.append(int(xx))
            #print(_tempinp.pfile.node_id(xx), end = '     ')


        #Add an empty object belong to class'Inputdata()' as the i th element in list _INP0
        _INP0.append(Inputdata())     
        #Add values to _INP0[i] from _tempinp
        _INP0[i].fname = _tempinp.fname
        _INP0[i].Outfname = _tempinp.Outfname
        _INP0[i].pfile = _tempinp.pfile
        _INP0[i].stmod =_tempinp.stmod
        _INP0[i].scalar = _tempinp.scalar
        _INP0[i].Nodelist = _tempinp.Nodelist
        _INP0[i].OutDIR = _tempinp.OutDIR




        #judge whether the nodes are the same in different files
        if _judgeInpN == 0:
            if input("Is node to be applied for each postfile the same?(Y/N)") == "Y":
                _judgeInpN = 2
                pass
            else:
                _judgeInpN = 1

        #############################################
        #FOR TEST
        #print("............../nAT THE END OF this round, JudgeInpN = %d" % _judgeInpN)
        #input()
        #############################################

    #until here, item'scalar' and item'dic' are still remained as vacant
    return (_INP0)

def define_item(_stmod, _INP0, _filenamelist, judgeI):
    judgeI
    _itemmodlist=[]
    #Choose Working mode
    #_itemmodelist: a list includes n lists(n is the number of postfiles.) while every sublists contains the index of scalar type in need.
    print("\nPLEASE CHOOSE THE item you want to get from the postfile\n")
    print("\nIf you don't know the identical numbers of items contained in every module, Please choose the Manual Mode and check it out later.")
    print("Are you sure to continue?\n1. CONTINUE \n\n2. CHANGE TO MANUAL MODE \n\n3. RESTART\n")
    JudgeCON = switch(1,3,0)
    if JudgeCON == 1:
        pass
    elif JudgeCON == 2:
        print("Only the file with the 1st inputed filename will be opened")
        input()
        judgeI =1
    else:
        print("RESTART!!!\n")
        return()
    
    #Show the items which can be chosen to be exported
    if _stmod == 1:
        for x in range(0,_INP0[0].pfile.node_scalars()):
            print("%2d. %s" % (x,_INP0[0].pfile.node_scalar_label(x)))
        pass
    elif _stmod == 3:
        for x in range(0, _INP0[0].pfile.element_scalars()):
            print("%2d. %s" % (x,_INP0[0].pfile.element_scalar_label(x)))
        pass


    if (input("Is items to be print from each postfile the same?(Y/N)") == 'Y') :
        #adapting the same 'tempd' (selected item) for each post-file
        while True:
            tmpstr = input("Please typein the item(s):")
            tmplist = tmpstr.split()
            if len(tmplist) == 0:
                print("Input Error!")
                continue
            tmpIntList = []
            for x in tmplist:
                tmpIntList.append(int(x))
            for x in _filenamelist:
                _itemmodlist.append(tmpIntList)
            break

    else:
        print("PLEASE Type in the items of each file")        
        for x in _filenamelist:
            tmplist = input("file %s\t:\n" % _INP0.fname).split()
            if len(tmplist) == 0 :
                break  
            tmpIntList = []
            for x in tmplist:
                if len(_itemmodlist)>=len(_filenamelist):
                    break
                tmpIntList.append(int(x))
                _itemmodlist.append(tmpIntList)
    return(_itemmodlist)

def preex(stmod, judgeI):
    #Get current date and time TO NAME THE OUTPUTFILE DIR
    current_time = datetime.datetime.now()
    date_string = current_time.strftime("%Y-%m-%d_%H-%M-%S")
    OutDIR = "result/%s" % (date_string)
    #Pre-executing process
    #input data
    #Parameter stmod:TYPE of Output-Data that you Expected(NODE-VECTOR/NODE-SCALAR\ELEMENT SCALAR\)



    #Define Object'INP0' to store the readed-in post file using class'Inputdata'
    #INP0 = Inputdata()

    filenamelist = input_fname(judgeI)      #filenamelist: string x N rows

    #Giving the length of filenamelist(times to repet importing the file)
    if judgeI == 1:     #(selecting '1.manual')
        LEN = 1
        pass
    else:
        LEN = len(filenamelist)
    
    #Define INP0
    INP0 = []
    print("\n")
    print("LEN IS %d \n\nPlease input the nodelist of each work:" % LEN)
    
    #Readin file and add node

    INP0=read_in(filenamelist, LEN, OutDIR)
    if INP0 == 0:
        return 0

    print("TESTPOINT1")
    #input("TEST")
    
    itemmodlist=define_item(stmod, INP0, filenamelist, judgeI)
    
    ##############################
    print("LEN of INP0 = %d" % len(INP0))
    print("LEN of itemmodlist is %d" % len(itemmodlist))
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #############################

    #############################
    #Get the number of increments for each file
    print("-----------------------------------------------------")
    print("Please difine the number of increments in each file. If you want to get all increments , please type '0':\n")
    maxinc = input_MaxInc(LEN)

    for i in range(0, LEN):
        INP0[i].scalar = itemmodlist[i]
        INP0[i].stmod = stmod
        INP0[i].maxInc = maxinc[i]
        for x in INP0[i].Nodelist:
            print(x, end = '    ')
        print('\n')
    return INP0