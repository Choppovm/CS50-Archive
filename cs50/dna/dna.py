import csv
import sys

def main():
    if len(sys.argv) < 3:
        print("Usage: python dna.py *.csv *.txt")
        sys.exit(1)
    d = []
    with open(sys.argv[1], 'r') as file:
        r = csv.DictReader(file)
        for row in r:
            d.append(row)
    with open(sys.argv[2], 'r') as file:
        dnas = file.read()
    subss = list(d[0].keys())[1:]
    result = {}
    for subs in subss:
        result[subs] = longest_match(dnas, subs)
    for person in d:
        match = 0
        for subs in subss:
            if int(person[subs]) == result[subs]:
                match += 1
        if match == len(subss):
            print(person["name"])
            return
    print("No match")
    return
def longest_match(seq, sseq):
    lr = 0
    sslen = len(sseq)
    slen = len(seq)
    for i in range(slen):
        c = 0
        while True:
            start = i + c * sslen
            end = start + sslen
            if seq[start:end] == sseq:
                c += 1
            else:
                break
        lr = max(lr, c)
    return lr
main()
