#!/usr/bin/python
from collections import defaultdict
import re

state = 'oslc elai tant myse'
# state = 'to fu'
# wordlist = 'testwords.txt'
wordlist = 'bsd_wordlist.txt'
LETTERS = state.replace(' ', '')
LETTER_SET = set(i for i in LETTERS)
COL_LEN = int(len(LETTERS)**(.5))
def grid(b):
    return b.split(' ')

def matrix():
    return [[l for l in i] for i in grid(state)]

def breakdown_word(word):
    """Use string slices to get all combos of a word"""
    return [word[:i+1]for i in range(len(word))]

def load_words():
    """"""
    d = defaultdict(set)
    with open(wordlist) as words:
        for word in words:
            word = word.lower().rstrip('\n')
            if len(word) <= len(LETTERS):
               for k in breakdown_word(word):
                   d[k].add(word)
        return d

def check_valid(move):
    return True if move[0] >= 0 and move[0] < COL_LEN and move[1] >= 0 and move[1] < COL_LEN else False

def add_sets(a, b):
    return (a[0]+b[0], a[1]+b[1])

m = matrix()
onboard = set()
movesets = [(1,0), (0,1), (-1,0), (0,-1), (-1,-1), (1,1), (-1,1), (1,-1)]
word_set = load_words()

def xy_to_words(coordinates):
    word = ''
    for coord in coordinates:
        word += m[coord[0]][coord[1]]
    return word

def traverse(x, y, visited=None):
    letter = m[x][y]
    origin = (x,y)
    if visited is None:
        # to create a new visited param after first initialized
        visited = [origin]
    next_move = [add_sets(origin, n) for n in movesets if check_valid(add_sets(origin, n))]
    # print(origin, next_move)
    for move in next_move:
        # simport ipdb; ipdb.set_trace()
        if (move not in visited):
            path = visited + [move]
            # check next word if possible, if so continue
            possibility = xy_to_words(path)
            if possibility in word_set:
                onboard.add(xy_to_words(path))
                traverse(move[0], move[1], path)


if __name__ == '__main__':
# def main():
    possibilities = {}
    # Build word possibilities
    for x, row in enumerate(grid(state)):
        for y, letter in enumerate(row):
            print(x,y,letter)
            traverse(x,y)
            # traverse(x,y, visited)

    print(len(onboard))

# if __name__ == '__main__':
#     main()
