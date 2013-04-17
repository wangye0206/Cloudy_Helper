# DataGather.py can merge temporary files generate by 'grid' command.
# This is used when Cloudy fails to merge those files together.
# To use this script, put those temporary file in './origina_data/'
# Run 'DataGather.py point_num file_name1 file_name2 ...'
# Here the point_num is the total points you calculat with cloudy,
# and file_name are the files you want to save.
# For example, if you calculate 1000 points
# and use "save overview 'test.ovr'" command,
# run 'DataGather.py 1000 test.ovr' in your terminal
# We don't suggest mergint standard output of Cloudy together,
# since that file may very big.


#!/usr/bin/env python3

import sys, threading

class Process(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print('Thread \'{}\' start!'.format(self.FileName))
        File = open('./{}'.format(self.FileName), 'w')

        HeaderPath = './original_data/{}'.format(self.FileName)
        if( not os.path.exists(Headerpath) ):
            print('{} header missing!'.format(self.FileName))
            return 0
        HeadFile = open('./original_data/{}'.format(self.FileName))
        Head = HeadFile.readline()
        HeadFile.close()
        File.write('{}'.format(Head))

        check = 0
        for FileNum in range(SubFileNum):
            SubFilePath = './original_data/grid{0:09d}_{1}'.format(FileNum, self.FileName)
            if( os.path.exists(SubFilePath) ):
                check += 1
                SubFile = open(SubFilePath, 'r')
                Lines = SubFile.readlines()
                SubFile.close()
                for LineNum in range(0, len(Lines)):
                    File.write('{}'.format(Lines[LineNum]))
        File.close()

        if( check < self.SubFileNum ):
            print('Some data in file {} are missing!\n Cloudy may not finish calculation phase before this script is run.'.format(self.FileName))
            
        return 0

def main():
    # Check whether arguments are provided
    if( len( sys.argv )<2 ):
        sys.exit('ERROR: I don\'t get all arguments I need!\nPlease provide total points number and file names.')

    PointsNum = sys.argv[1]

    # Get files list need ot merge
    Files = sys.argv[2:]
    
    threads = []
    for i in Files:
        thread_i = Process()
        threads += [thread_i]
        thread_i.FileName = i
        thread_i.SubFileNum = PointsNum
        thread_i.start()

    for t in threads:
        t.join()

if __name__ == '__main__':
    main()
