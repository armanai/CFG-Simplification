from Grammar import Grammar


def main():
    f = open("grammar3.txt", "r")
    grammar = ""
    lines = f.readlines()

    for line in lines:
        if '->' not in line:
            raise Exception('File does not contain a valid grammar production rules.')
        else:
            grammar += line

    Grammar(grammar)


if __name__ == "__main__":
    main()