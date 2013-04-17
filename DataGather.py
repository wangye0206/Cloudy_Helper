#!/usr/bin/env python3

import sys, os, math, threading

class Process(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print('Thread {} start!'.format(self.Postfix))
        File = open('./final3.{}'.format(self.Postfix), 'w')
        HeadFile = open('./original_data/final3.{}'.format(self.Postfix))
        Head = HeadFile.readline()
        HeadFile.close()
        File.write('{}'.format(Head))
        total = 234390
        for FileNum in range(total):
            SubFile = open('./original_data/grid{0:09d}_final3.{1}'.format(FileNum, self.Postfix), 'r')
            Lines = SubFile.readlines()
            SubFile.close()
            for LineNum in range(0, len(Lines)):
                File.write('{}'.format(Lines[LineNum]))
        File.close()
        return 0

def main():
    kind = ['col', 'ovr', 'cole', 'grd']
    threads = []
    for i in kind:
        thread_i = Process()
        threads += [thread_i]
        thread_i.Postfix = i
        thread_i.start()

    for t in threads:
        t.join()

if __name__ == '__main__':
    main()
