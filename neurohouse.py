import sys
import codecs
from py.general import pattern
from py.general import post_data

def main():
    if __name__ == "__main__":
        f = open('logs.log', 'a')
        sys.stderr = f
        if len(sys.argv) > 1:
            sys.stdout = f
            pattern(sys.argv[1])()
        else:
            # Режим дебага
            sys.stdout = f
            pattern('-e')()
        f.close()

main()

