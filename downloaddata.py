import stockdata as sd
import sys

if __name__ == '__main__':
    dt = sys.argv[1] if len(sys.argv) == 2 else '2015-01-01'
    sd.download(startdt={dt})
