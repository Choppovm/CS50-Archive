import csv
import itertools
import sys

PROBS = {
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },
    "trait": {
        2: {
            True: 0.65,
            False: 0.35
        },
        1: {
            True: 0.56,
            False: 0.44
        },
        0: {
            True: 0.01,
            False: 0.99
        }
    },
    "mutation": 0.01
}


def m():
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])
    prob = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }
    names = set(people)
    for haveT in pset(names):
        fevidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in haveT))
            for person in names
        )
        if fevidence:
            continue
        for oneG in pset(names):
            for twoG in pset(names - oneG):
                p = joint_probability(people, oneG, twoG, haveT)
                update(prob, oneG, twoG, haveT, p)
    normalize(prob)
    for person in people:
        print(f"{person}:")
        for field in prob[person]:
            print(f"  {field.capitalize()}:")
            for value in prob[person][field]:
                p = prob[person][field][value]
                print(f"    {value}: {p:.4f}")

def load_data(filename):
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data

def pset(s):
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]

def joint_probability(people, oneG, twoG, haveT):
    joint_prob = 1
    for person in people:
        person_prob = 1
        pg = (2 if person in twoG else 1 if person in oneG else 0)
        pt = person in haveT
        mother = people[person]['mother']
        father = people[person]['father']
        if not mother and not father:
            person_prob *= PROBS['gene'][pg]
        else:
            mother_prob = inherit_prob(mother, oneG, twoG)
            father_prob = inherit_prob(father, oneG, twoG)
            if pg == 2:
              person_prob *= mother_prob * father_prob
            elif pg == 1:
              person_prob *= (1 - mother_prob) * father_prob + (1 - father_prob) * mother_prob
            else:
              person_prob *= (1 - mother_prob) * (1 - father_prob)
        person_prob *= PROBS['trait'][pg][pt]
        joint_prob *= person_prob
    return joint_prob


def inherit_prob(pn, oneG, twoG):
    if pn in twoG:
        return 1 - PROBS['mutation']
    elif pn in oneG:
        return 0.5
    else:
        return PROBS['mutation']

def update(prob, oneG, twoG, haveT, p):
    for person in prob:
        pg = (2 if person in twoG else 1 if person in oneG else 0)
        pt = person in haveT
        prob[person]['gene'][pg] += p
        prob[person]['trait'][pt] += p

def normalize(prob):
        for person in prob:
            gps = sum(prob[person]['gene'].values())
            tps = sum(prob[person]['trait'].values())
            prob[person]['gene'] = { genes: (prob / gps) for genes, prob in prob[person]['gene'].items()}
            prob[person]['trait'] = { trait: (prob / tps) for trait, prob in prob[person]['trait'].items()}

if __name__ == "__m__":
    m()
