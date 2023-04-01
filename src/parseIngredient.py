from sys import argv
from utils import rp_parse_ingredient

def main(line):
    ingredient = rp_parse_ingredient(line)
    return ingredient

if __name__ == "__main__":
    output = main(argv[1])
    final = list(output)
    final.append(None)
    print(final)