#!/usr/bin/python
from collections import defaultdict
import re


class Boggle():

    def __init__(self, state, wordlist):

        self.state = state
        # CONSTANTS
        self.MOVESETS = [(1,0), (0,1), (-1,0), (0,-1), (-1,-1), (1,1), (-1,1), (1,-1)]
        self.MIN_LETTERS = 3
        self.LETTERS = state.replace(' ', '')
        self.LETTER_SET = set(i for i in self.LETTERS)
        self.COL_LEN = int(len(self.LETTERS)**(.5))

        # SETUP GAME OBJECTS
        self.m = self.matrix()
        self.word_set = self.load_words(wordlist)
        self.onboard = set()

        # Solve Board
        for x, row in enumerate(self.grid(state)):
            for y, letter in enumerate(row):
                print(x,y,letter)
                self.traverse(x,y)

    def add_pair(self, a, b):
        return (a[0]+b[0], a[1]+b[1])

    def breakdown_word(self, word):
        """Use string slices to get all combos of a word"""
        return [word[:i+1]for i in range(len(word))]

    def check_valid(self, move):
        return True if move[0] >= 0 and move[0] < self.COL_LEN and move[1] >= 0 and move[1] < self.COL_LEN else False

    def grid(self, rows):
        return rows.split(' ')

    def load_words(self, wordlist):
        """"""
        d = defaultdict(set)
        with open(wordlist) as words:
            for word in words:
                word = word.lower().rstrip('\n')
                if len(word) <= len(self.LETTERS) and len(word) >= self.MIN_LETTERS:
                   for k in self.breakdown_word(word):
                       d[k].add(word)
            return d

    def matrix(self):
        return [[l for l in i] for i in self.grid(self.state)]

    def traverse(self, x, y, visited=None):
        origin = (x,y)
        if visited is None:
            # to create a new visited param after first initialized
            visited = [origin]

        # Get valid move list
        next_moves = [self.add_pair(origin, n) for n in self.MOVESETS if self.check_valid(self.add_pair(origin, n))]

        # Test each next move
        for move in next_moves:
            if (move not in visited):
                path = visited + [move]
                # check next word if possible, if so continue
                possibility = self.xy_to_words(path)
                if possibility in self.word_set:
                    if possibility in self.word_set.get(possibility):
                        self.onboard.add(self.xy_to_words(path))
                    self.traverse(move[0], move[1], path)

    def xy_to_words(self, coordinates):
        word = ''
        for coord in coordinates:
            word += self.m[coord[0]][coord[1]]
        return word

# def main():
if __name__ == '__main__':
    state = 'oslc elai tant myse'
    wordlist = 'bsd_wordlist.txt'
    # state = 'to fu'
    # wordlist = 'testwords.txt'

    board = Boggle(state, wordlist)

    print('num words on the board:', len(board.onboard))

# if __name__ == '__main__':
#     main()
