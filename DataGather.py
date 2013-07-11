#!/usr/bin/env python3

######################################################################### 
# DataGather.py can merge temporary files generate by 'grid' command.   # 
# This is used when Cloudy fails to merge those files together.         # 
# Synopsis:  ./DataGather.py (original_data_path) file1 file2 ...       #
# original_data_path is a optional argument, it must end with '/'       #
# its default value is './original_data/',                              # 
# file1, file2 and ... are the files you want to save.                  # 
# We don't suggest mergint standard output of Cloudy together,          # 
# since that file may very big.                                         # 
#########################################################################

import sys, threading, os

class Process(threading.Thread):
    def __init__(self, SubFilePath, FileName):
        threading.Thread.__init__(self)
        self.SubFilePath = SubFilePath
        self.FileName = FileName

    def run(self):
        print('Thread \'{}\' start!'.format(self.FileName))
        
        FileExist = 1
        FileNum = 0
        FileSequence = 0
        Check = 0
        Data = []

        if( self.FileName.find('.out') == -1 ):
            TitleFile = open('{0}{1}'.format(self.SubFilePath, self.FileName))
            TitleLines = TitleFile.readlines()
            TitleFile.close()
            if( TitleLines == 0 ):
                print('{0} title is missing'.format(self.FileName))
            else:
                for TitleLineNum in range(0, len(TitleLines)):
                    Data.append(TitleLines[TitleLineNum])

        while( FileExist == 1 ) :
            if( os.path.exists('{0}grid{1:09d}_{2}'.format(self.SubFilePath, FileSequence, self.FileName)) ):
                SubFile = open('{0}grid{1:09d}_{2}'.format(self.SubFilePath, FileSequence, self.FileName), 'r')
                Lines = SubFile.readlines()
                SubFile.close()
                if (len(Lines) == 0):
                    Data.append('\n')
                else:
                    for LineNum in range(0, len(Lines)):
                        Data.append(Lines[LineNum])
                FileNum += 1
                Check = 0
            else:
                Check += 1
                if( Check == 1000 ):
                    FileExist = 0
            FileSequence += 1

        File = open('./{}'.format(self.FileName), 'w')
        for i in Data:
            File.write('{}'.format(i))
        File.close()

        if( FileNum == 0 ):
            print('ERROR: I cannot find any {} file, please check path!'.format(self.FileName))
        else:
            print('Thread \'{0}\' finished! {1} files are merged together'.format(self.FileName, FileNum))
        return 0

        
def main():
    # Check whether arguments are provided
    if( len( sys.argv )<2 ):
        sys.exit('ERROR: I don\'t get all arguments I need!\nPlease provide file names.')

    # Default Data Path
    Path = './original_data/'

    # Get Argumetns
    Arguments = sys.argv[1:]
    Files = []

    for ArgvNum in range( len(Arguments) ):
        if( Arguments[ArgvNum].endswith('/') ):
            Path = Arguments[ArgvNum]
        else:
            Files.append( Arguments[ArgvNum] )

    if( not os.path.isdir(Path) ):
        sys.exit('ERROR: I cannot find where are the data files!\nPlease input path to folder which contains the data files and make sure it end with \'/\'.')
    
    threads = []
    for i in Files:
        thread_i = Process(Path,i)
        threads += [thread_i]
        thread_i.start()

    for t in threads:
        t.join()

if __name__ == '__main__':
    main()
