#!/usr/bin/env python

import re
from collections import defaultdict
from threading import Timer
from six.moves import input


class Boggle():
    """ Game based on a 4x4 Grid where you can form words using adjacent tiles.
    Connecting tiles may only be used once per word and all valid words on are
    initialized by the wordlist.
    """

    def __init__(self, state, wordlist):

        self.state = state
        # CONSTANTS
        self.MOVESETS = [(1, 0), (0, 1), (-1, 0), (0, -1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
        self.MIN_LETTERS = 3
        self.LETTERS = state.replace(' ', '')
        self.LETTER_SET = ''.join(set(i for i in self.LETTERS))
        self.LETTER_REGEX = re.compile(r"\b[" + self.LETTER_SET + r"]{1,}\b")

        self.COL_LEN = int(len(self.LETTERS)**(.5))

        # SETUP GAME OBJECTS
        self.matrix = self._build_matrix()
        self.word_set = self._load_words(wordlist)
        self.on_board = set()

        # Solve Board
        for x, row in enumerate(self.state.split(' ')):
            for y, _ in enumerate(row):
                self._traverse(x, y)

    def _add_pair(self, a, b):
        """Add two coordinate pairsets together"""
        return (a[0]+b[0], a[1]+b[1])

    def _breakdown_word(self, word):
        """Use string slices to get all combos of a word from left to right"""
        return [word[:i+1]for i in range(len(word))]

    def _check_valid(self, move):
        """Check is move is a valid move and not out of bounds for matrix"""
        return True if move[0] >= 0 and move[0] < self.COL_LEN and move[1] >= 0 and move[1] < self.COL_LEN else False

    def _check_letters(self, word):
        """Determines if letters are in word_set """
        return self.LETTER_REGEX.match(word)

    def check_guess(self, guess):
        """Checks if word is on board"""
        return guess in self.on_board

    def _load_words(self, wordlist):
        """Load words from a wordlist file"""
        d = defaultdict(set)
        with open(wordlist) as words:
            for word in words:
                word = word.lower().rstrip('\n')
                if len(word) <= len(self.LETTERS) and len(word) >= self.MIN_LETTERS and self._check_letters(word):
                    for k in self._breakdown_word(word):
                        d[k].add(word)
            return d

    def _build_matrix(self):
        """Get a 2D Matrix representation of the board state"""
        return [[l for l in i] for i in self.state.split(' ')]

    def _traverse(self, x, y, visited=None):
        """Use a trie strategy with backrefs to previous passed positions until done"""
        origin = (x, y)
        if visited is None:
            # to create a new visited param after first initialized
            visited = [origin]

        # Get valid move list
        next_moves = [self._add_pair(origin, n) for n in self.MOVESETS if self._check_valid(self._add_pair(origin, n))]

        # Test each next move
        for move in next_moves:
            if move not in visited:
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

    def score_word(self, word):
        """Scores a word"""
        return len(word)

    def score_word_set(self, words):
        """Scores a set of words"""
        return sum(self.score_word(w) for w in words)


class GameView():
    """CLI window for Displaying Game logic"""

    def __init__(self, board):
        self.board = board
        self.matrix = board.matrix

        # CONSTANTS
        self.TIME_LIMIT = 90

        # Game Objects
        self.game_running = False
        self.guesses = set()
        self.correct = set()

    def display_board(self):
        """Print out the board space delimited with newline at bottom"""
        for row in self.matrix:
            print(' '.join(row))

    def _end_game(self):
        """Display the Results"""
        self.game_running = False
        print('\n\n')
        print('Your score is: ', self.board.score_word_set(self.correct))
        print('The words you got correct: ', self.get_correct())
        print('The number of words you guessed: ', len(self.guesses))
        print('Number of possible words on the Board:', len(self.board.on_board))

    def get_correct(self):
        """Getter and formatter for words present on wordlist"""
        return ' '.join(self.correct)

    def _start_timer(self):
        """Start a timer, when it returns we want to tell the user the score"""
        self.game_running = True
        t = Timer(self.TIME_LIMIT, self._end_game)
        t.start()

    def run(self):
        """Starts the Game"""
        print('Starting game\n\n')
        self._start_timer()
        while self.game_running is True:
            self.display_board()
            guess = input('\nA guess?: ')

            if self.game_running is True:
                if self.board.check_guess(guess):
                    self.correct.add(guess)
                self.guesses.add(guess)
            else:
                print('Game Over!')


def main():
    """Game Starts Here"""
    state = 'oslc elai tant myse'
    wordlist = 'bsd_wordlist.txt'

    board = Boggle(state, wordlist)
    game = GameView(board)
    game.run()

if __name__ == '__main__':
    main()
