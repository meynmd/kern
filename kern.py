from __future__ import print_function
import string
import math
import sys
import itertools

NonSem = ['!', '*']
Delim = '\t'

class Reader:
    def __init__(self):
        self.kernData = ''
        self.measures = []



    def Read(self, filename):
        with open(filename, 'r') as fp:
            self.kernData = fp.readlines()

        measureData = []
        measureNum = 1
        for line in self.kernData:
            if line[0] in NonSem:
                continue
            elif line[0] == '=':
                self.measures.append(Measure(measureData, measureNum))
                measureData = []
                measureNum += 1
            else:
                measureData.append(line.split('\t'))



    def ReadNotes(self, data):
        notes = data.split(Delim)


    def GetRawData(self):
        return self.kernData



class Measure:
    def __init__(self, data = None, num = None, meter = None, parts = None):
        self.number = num
        self.meter = (4., 4.)
        self.numParts = parts
        self.pitches = []
        self.durations = []
        if data != None:
            self.ReadData(data)

    def ReadData(self, lines):
        # given lines: row->timeslice, col->part
        self.numParts = len(lines[0])
        noteVals = [[0.
                     for j in range(len(lines))
                     ] for i in range(self.numParts)]

        # set up noteVals: row->part, col->timeslice
        for j, line in enumerate(lines):
            for i, part in enumerate(line):
                # find numbers to indicate note values
                val = filter(lambda x: x in string.digits, part)
                if len(val) == 0:
                    noteVals[i][j] = 0.
                else:
                    val = float(str(val))
                    noteVals[i][j] = val

                    # make alterations for dotted notes
                    for k in range(part.count('.')):
                        val *= 1. / 3.
                        noteVals[i][j] -= val

        print(self.number)
        for r in noteVals:
            print(r)
        print('\n')

        # validation
        valueTotal = [sum([1./v for v in row if v != 0]) for row in noteVals]
        if self.meter != None:# and self.number != None:
            for t in valueTotal:
                if math.fabs(t - self.meter[0] / self.meter[1]) > 0.01:
                    print('Warning: note values in measure {0} '\
                        'do not sum to expected value'.format(
                        self.number), file = sys.stderr)






    def Print(self):
        print('Measure #{0}\t\t{1} beats\t\t{2} parts'.format(
            self.number, self.meter, self.numParts))


