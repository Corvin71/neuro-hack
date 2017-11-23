import sys
import codecs
from py.general import pattern
from py.general import post_data

def main():
    if __name__ == "__main__":
        f = open('logs.log', 'a')
        if len(sys.argv) > 1:
            sys.stdout = f
	    sys.stderr = f
            pattern(sys.argv[1])()
        else:
            # Без параметров выводится справка
            pattern('-h')()
        f.close()

main()

