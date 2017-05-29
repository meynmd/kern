import sys
from kern import Reader
import params

if __name__ == '__main__':
    filename = sys.argv[1]
    path = params.datapath + filename
    kr = Reader()
    kr.Read(path)
