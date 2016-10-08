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
        self.matrix = self._build_matrix()
        self.word_set = self._load_words(wordlist)
        self.on_board = set()

        # Solve Board
        for x, row in enumerate(self.state.split(' ')):
            for y, letter in enumerate(row):
                print(x,y,letter)
                self._traverse(x,y)

    def _add_pair(self, a, b):
        """Add two coordinate pairsets together"""
        return (a[0]+b[0], a[1]+b[1])

    def _breakdown_word(self, word):
        """Use string slices to get all combos of a word from left to right"""
        return [word[:i+1]for i in range(len(word))]

    def _check_valid(self, move):
        """Check is move is a valid move and not out of bounds for matrix"""
        return True if move[0] >= 0 and move[0] < self.COL_LEN and move[1] >= 0 and move[1] < self.COL_LEN else False

    def _load_words(self, wordlist):
        """Load words from a wordlist file"""
        d = defaultdict(set)
        with open(wordlist) as words:
            for word in words:
                word = word.lower().rstrip('\n')
                if len(word) <= len(self.LETTERS) and len(word) >= self.MIN_LETTERS:
                   for k in self._breakdown_word(word):
                       d[k].add(word)
            return d

    def _build_matrix(self):
        """Get a 2D Matrix representation of the board state"""
        return [[l for l in i] for i in self.state.split(' ')]

    def _traverse(self, x, y, visited=None):
        """Use a trie strategy with backrefs to previous passed positions until done"""
        origin = (x,y)
        if visited is None:
            # to create a new visited param after first initialized
            visited = [origin]

        # Get valid move list
        next_moves = [self._add_pair(origin, n) for n in self.MOVESETS if self._check_valid(self._add_pair(origin, n))]

        # Test each next move
        for move in next_moves:
            if (move not in visited):
                path = visited + [move]
                # check next word if possible, if so continue
                possibility = self._xy_to_words(path)
                if possibility in self.word_set:
                    if possibility in self.word_set.get(possibility):
                        self.on_board.add(self._xy_to_words(path))
                    self._traverse(move[0], move[1], path)

    def _xy_to_words(self, coordinates):
        """Translate a set of matrix coordinates in order into a word"""
        word = ''
        for coord in coordinates:
            word += self.matrix[coord[0]][coord[1]]
        return word

# def main():
if __name__ == '__main__':
    state = 'oslc elai tant myse'
    wordlist = 'bsd_wordlist.txt'
    # state = 'to fu'
    # wordlist = 'testwords.txt'

    board = Boggle(state, wordlist)

    print('num words on the board:', len(board.on_board))

# if __name__ == '__main__':
#     main()
