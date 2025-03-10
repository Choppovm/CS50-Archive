import sys
from crossword import *

class CrosswordCreator():

    def __init__(self, crossword):
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )
        img.save(filename)

    def solve(self):
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        for var in self.domains:
            for word in set(self.domains[var]):
                if len(word) != var.length:
                    self.domains[var].remove(word)

    def revise(self, x, y):
        revised = False
        i, j = self.crossword.overlaps[x, y]
        for x_word in set(self.domains[x]):  # Iterate over a copy to avoid modification issues
            if not any(x_word[i] == y_word[j] for y_word in self.domains[y]):
                self.domains[x].remove(x_word)
                revised = True
        return revised

    def ac3(self, arcs=None):
        if arcs is None:
            arcs = list()
            for x in self.domains:
                for y in self.crossword.neighbors(x):
                    arcs.append((x, y))
        while arcs:
            x, y = arcs.pop()
            if self.revise(x, y):
                if not self.domains[x]:
                    return False
                for z in self.crossword.neighbors(x) - {y}:  # Corrected subtraction
                    arcs.append((z, x))
        return True

    def assignment_complete(self, assignment):
        return not bool(self.crossword.variables - set(assignment))

    def consistent(self, assignment):
        used_words = set()
        for var in assignment:
            if assignment[var] not in used_words:
                used_words.add(assignment[var])
            else:
                return False
            if len(assignment[var]) != var.length:
                return False
            for neighbor in self.crossword.neighbors(var):
                if neighbor in assignment:
                    i, j = self.crossword.overlaps[var, neighbor]
                    if assignment[var][i] != assignment[neighbor][j]:
                        return False
        return True

    def order_domain_values(self, var, assignment):
        n = dict()
        for value in self.domains[var]:
            n[value] = 0
            for neighbor in {neighbor for neighbor in self.crossword.neighbors(var) if neighbor not in assignment}:
                if value in self.domains[neighbor]:
                    n[value] += 1
        return sorted(n, key=n.get)

    def select_unassigned_variable(self, assignment):
        best = None
        for var in self.crossword.variables - set(assignment):
            if (
                best is None or
                len(self.domains[var]) < len(self.domains[best]) or
                len(self.crossword.neighbors(var)) > len(self.crossword.neighbors(best))
            ):
                best = var
        return best

    def backtrack(self, assignment):
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.domains[var]:
            assignment[var] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result is not None:
                    return result
            assignment.pop(var)
        return None

def main():
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)

if __name__ == "__main__":
    main()
