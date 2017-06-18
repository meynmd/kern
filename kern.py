from __future__ import print_function
import string
import math
import sys
import itertools

NonSem = ['!', '*']
Delim = '\t'
Pitches = {'A' : 0, 'B' : 2, 'C' : 3, 'D' : 5, 'E' : 7, 'F' : 8, 'G' : 10}

class Reader:
    def __init__(self):
        self.data = ''
        self.measures = []


    def Read(self, filename):
        with open(filename, 'r') as fp:
            self.data = fp.readlines()

        lines = []
        measureNum = 1
        for line in self.data:
            if line[0] in NonSem:
                continue
            elif line[0] == '=':
                self.measures.append(Measure(lines, measureNum))
                lines = []
                measureNum += 1
            else:
                lines.append(line.split('\t'))

        return self.measures


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
        vals = [[(0, 0) for j in range(len(lines))]
                for i in range(self.numParts)]
        pitches = [[(None, None) for j in range(len(lines))]
                   for i in range(self.numParts)]

        # set up noteVals: row->part, col->timeslice
        for j, line in enumerate(lines):
            for i, part in enumerate(line):
                vals[i][j] = self.ReadValue(part)
                pitches[i][j] = self.ReadPitch(part)

        print(self.number)
        for i in range(len(vals)):
            print(pitches[i])
            print(vals[i])
            print('\n')
        print('\n')

        self.validate(vals)


    def ReadPitch(self, enc):
        for i in range(len(enc)):
            if enc[i] in string.ascii_letters:
                break
        j = i
        while j < len(enc) - 1:
            if enc[j + 1] == enc[i]:
                j += 1
            else:
                break
        #         
        # for j in range(i, len(enc)):
        #     if enc[j] != enc[i]:
        #         break

        if enc[i].upper() in Pitches.keys():
            pitch = Pitches[enc[i].upper()]
            octave = j - i
            if enc[i] in string.ascii_uppercase:
                octave = -octave
            if j < len(enc) - 1:
                if enc[j + 1] == '#':
                    pitch = (pitch + 1) % 12
                elif enc[j + 1] == '-':
                    pitch = (pitch + 11) % 12
        else:
            pitch = None
            octave = None

        return (pitch, octave)


    def ReadValue(self, enc):
        # find numbers, which indicate note values
        val = filter(lambda x: x in string.digits, enc)
        if len(val) == 0:
            # there is no note at this position
            return (0, 0)
        else:
            # get base note value
            val = int(val)
            # get number of dots to add
            return (val, enc.count('.'))


    def validate(self, noteVals):
        # 2^-n (2^(n + 1) - 1)
        valueTotal = [
            sum([1. / v * 2.**(-d) * (2**(d + 1) - 1) for (v, d) in row if v != 0])
            for row in noteVals]

        if self.meter != None:
            self.number = None
            for t in valueTotal:
                if math.fabs(t - self.meter[0] / self.meter[1]) > 0.01:
                    print('Warning: note values in measure {} '\
                        'sum to {} instead of expected value {}'.format(
                        self.number, t, self.meter[0] / self.meter[1]),
                        file = sys.stderr)


    def Print(self):
        print('Measure #{0}\t\t{1} beats\t\t{2} parts'.format(
            self.number, self.meter, self.numParts))


