import itertools
import random

class Minesweeper():
    def __init__(self, height=8, width=8, mines=8):
        self.height = height
        self.width = width
        self.mines = set()
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True
        self.mines_found = set()
    def print(self):
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")
    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]
    def nearby_mines(self, cell):
        count = 0
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignorethe cell itself
                if (i, j) == cell:
                    continue
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1
        return count
    def won(self):
        return self.mines_found == self.mines

class Sentence():
    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count
    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count
    def __str__(self):
        return f"{self.cells} = {self.count}"
    def known_mines(self):
        if len(self.cells) == self.count:
            return set(self.cells)
        return set()
    def known_safes(self):
        if self.count == 0:
            return set(self.cells)
        return set()
    def mark_mine(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
            return 1
        return 0
    def mark_safe(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)
            return 1
        return 0

class MinesweeperAI():
    def __init__(self, height=8, width=8):
        self.height = height
        self.width = width
        self.moves_made = set()
        self.mines = set()
        self.safes = set()
        self.knowledge = []
    def mark_mine(self, cell):
        counter = 0
        self.mines.add(cell)
        for sentence in self.knowledge:
            counter += sentence.mark_mine(cell)
        return counter
    def mark_safe(self, cell):
        counter = 0
        self.safes.add(cell)
        for sentence in self.knowledge:
            counter += sentence.mark_safe(cell)
        return counter
    def add_knowledge(self, cell, count):
        self.moves_made.add(cell)
        self.mark_safe(cell)
        neighbors = set()
        i, j = cell
        for x in range(max(0, i-1), min(i+2, self.height)):
            for y in range(max(0, j-1), min(j+2, self.width)):
                if (x, y) != (i, j):
                    neighbors.add((x, y))
        self.knowledge.append(Sentence(neighbors, count))
        self.update_safes_and_mines()
        new_inferences = self.get_new_inferences()
        while new_inferences:
            for sentence in new_inferences:
                self.knowledge.append(sentence)
            self.update_safes_and_mines()
            new_inferences = self.get_new_inferences()
    def update_safes_and_mines(self):
        counter = 1
        while counter:
            counter = 0
            for sentence in self.knowledge:
                for cell in sentence.known_safes():
                    self.mark_safe(cell)
                    counter += 1
                for cell in sentence.known_mines():
                    self.mark_mine(cell)
                    counter += 1
            for cell in self.safes:
                counter += self.mark_safe(cell)
            for cell in self.mines:
                counter += self.mark_mine(cell)
    def get_new_inferences(self):
        new_inferences = []
        sentences_to_remove = []
        for set_1 in self.knowledge:
            if not set_1.cells:
                sentences_to_remove.append(set_1)
                continue
            for set_2 in self.knowledge:
                if not set_2.cells:
                    sentences_to_remove.append(set_2)
                    continue
                if set_1 != set_2:
                    if set_2.cells.issubset(set_1.cells):
                        diff_cells = set_1.cells.difference(set_2.cells)
                        diff_count = set_1.count - set_2.count
                        new_inference_to_add = Sentence(diff_cells, diff_count)
                        if new_inference_to_add not in self.knowledge:
                            new_inferences.append(new_inference_to_add)
        self.knowledge = [x for x in self.knowledge if x not in sentences_to_remove]
        return new_inferences
    def make_safe_move(self):
        for move in self.safes:
            if move not in self.moves_made and move not in self.mines:
                return move
        return None
    def make_random_move(self):
        for i in range(self.height):
            for j in range(self.width):
                move = (i, j)
                if move not in self.moves_made and move not in self.mines:
                    return move
        return None
