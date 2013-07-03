#!/usr/bin/env python3

import sys, os, math, queue, threading

def Process(Cole, Ovr):
    Data = []
    tot_line = len(Ovr)
            
    for LN in range( tot_line ):
        
        OvrColumns = Ovr[LN].split('\t')
        # hydrogen density
        hden = float(OvrColumns[3])
        # electron density
        eden = float(OvrColumns[4])

        ColeColumns = Cole[LN].split('\t')
        Temp = float(ColeColumns[1])
        hhe_cooling = 0.
        metal_cooling = 0.
        eeff = 0.
        other_cooling = 0.
        for i in range( 3, 50 ):
            if( i == 3 or i == 4 or i == 35 or i == 36 or i == 37 or i ==38 or i == 39 or i == 40 or i == 41 or i == 45 or i == 48 ):
                hhe_cooling += (float(ColeColumns[i])/(hden * eden))
            elif( i == 33 or i == 34 or i == 44 or i == 46 or i == 47 ):
                other_cooling += (float(ColeColumns[i]) / (hden * eden))
            elif( i == 43 ):
                eeff += float(ColeColumns[i])/(hden * eden)
            else:
                metal_cooling += (float(ColeColumns[i])  / (hden*eden))
        Data.append([Temp, hden, eden, hhe_cooling, metal_cooling, eeff, other_cooling])
        
    return Data

Result_Queue = queue.PriorityQueue()

class CalThread(threading.Thread):
    def __init__(self, Cole, Ovr, Num):
        threading.Thread.__init__(self)
        self.Cole = Cole
        self.Ovr = Ovr
        self.Num = Num

    def run(self):
        Data = Process(self.Cole, self.Ovr)
        Result_Queue.put([self.Num, Data])

def main():

    print('Reading Files')
    ModelName = sys.argv[1]
    ColeFile = open('./{}.cole'.format(ModelName), 'r')
    ColeLines = ColeFile.readlines()
    ColeFile.close()
    del ColeLines[0]
    OvrFile = open('./{}.ovr'.format(ModelName), 'r')
    OvrLines = OvrFile.readlines()
    OvrFile.close()
    del OvrLines[0]

    print('Checking Files')
    for i in range(1, len(ColeLines) - 1 ):
        if( ColeLines[i].find('not converged') != -1):
            del ColLines[i]
    if( len(ColeLines) != len(OvrLines) ):
        sys.exit('ERROR: Two original files do not contian same amount of points!')

    print('Calculating')
    points = 1000
    ThreadNum = 1 + (len( OvrLines ) // points)
    Threads = []
    for t in range(ThreadNum):
        if( t == (ThreadNum - 1 ) ):
            Thread_t = CalThread(ColeLines, OvrLines, t)
        else:
            Thread_t = CalThread(ColeLines[0:points], OvrLines[0:points], t)
            del ColeLines[0:points]
            del OvrLines[0:points]
        Threads += [Thread_t]
        Thread_t.start()

    for j in Threads:
        j.join()
    
    print('Exporting')
    Output = open('Splited_Cooling.dat', 'w')
    Output.write('Temperature\thden\teden\tH&He\tmetal\teeff\tother\n')
    while( not Result_Queue.empty() ):
        TempList = Result_Queue.get()
        OutputList = TempList[1]
        for LineNum in range( len(OutputList) ):
            for ColNum in range(7):
                Output.write('{:.4e}'.format(OutputList[LineNum][ColNum]))
                if( ColNum == 6):
                    Output.write('\n')
                else:
                    Output.write('\t')
    Output.close()

if __name__ == "__main__":
    main()
