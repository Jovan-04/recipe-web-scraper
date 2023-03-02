from sys import argv

def main(line):
    ingredient = ["ap flour", 1.5, "cup"] # just poc for how the ingredient might be returned
    return ingredient

if __name__ == "__main__":
    output = main(argv[1])
    print(output)