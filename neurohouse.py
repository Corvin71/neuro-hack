import sys
import codecs
from py.general import pattern
from py.general import debug

def main():
    if __name__ == "__main__":
        f = open('logs.log', 'a')
        sys.stderr = f
        if len(sys.argv) > 1:
            sys.stdout = f
            pattern(sys.argv[1])()
        else:
            # Режим дебага
            #pattern('-h')()
            debug()
        f.close()

main()
