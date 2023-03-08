from sys import argv
from utils import rp_parse_ingredient

def main(line):
    ingredient = rp_parse_ingredient(line) # we should really make a utils file or something like that so we can directly import this function
    return ingredient

if __name__ == "__main__":
    output = main(argv[1])
    print(list(output))