#[About]
#A solver for the game "Hit & Blow".
#
#[Algorithm]
#1. Creates a list `possible_patterns` of all of the possible solutions.
#2. while (True):
#       (a) Reads a "hint" from stdin. Here, a hint consists of an input to the game (i.e. chosen colors and their order) and the output from the game (i.e. the number of "hit"s and that of "blow"s).
#       (b) Removes elements from `possible_patterns` which are not consistent with the hint just read.
#       (c) If the number of patterns stored in `possible_patterns` has become unity, breaks the loop since we've gotten the final solution now.
#
#[Sample Problems]
#1. |https://youtu.be/ahRHGTcBuhg?t=6456|
#
#[Sample Inputs and Outputs]
# <number>... <num_hit> <num_blow>: 0 3 5 2 1 2
# Possible Patterns: 72
# 
# <number>... <num_hit> <num_blow>: 1 2 5 3 1 1
# Possible Patterns: 8
# 
# <number>... <num_hit> <num_blow>: 3 1 5 0 0 3
# Possible Patterns: 1
#  (0, 5, 4, 3)
# 
# Solved.

import itertools
import math
import numpy as np

#parameters {

class Namespace:
    pass
ns: Namespace = Namespace()

ns.num_color: int = 6 #the number of possible colors (0, 1, 2, ..., ns.num_color - 1)
ns.num_choice: int = 4 #the number of colors which are chosen at once

ns.num_printed_possible_pattern: int = 5

#} parameters

#The number of possible solutions at the start of a game can be calculated analytically.
total_num_possible_pattern: int = math.comb(ns.num_color, ns.num_choice) * math.factorial(ns.num_choice)

#first row: A list of possible patterns.
#second row: A list of bool values. `False` means the corresponding element in the first row will be removed soon because it's not consistent with the hint.
possible_patterns: np.ndarray = np.empty((2, total_num_possible_pattern), dtype = object)
possible_patterns[1] = True

num_pattern: int = 0
for i in itertools.permutations(range(ns.num_color), ns.num_choice):
    possible_patterns[0][num_pattern] = i
    num_pattern += 1

assert (num_pattern == total_num_possible_pattern)

def IsValidInput(a: np.ndarray) -> bool: #{

    if (len(a) != ns.num_choice + 2):
        return False

    colors: np.ndarray = a[:-2]
    hint: np.ndarray = a[-2:]

    if (np.count_nonzero((0 <= colors) & (colors < ns.num_color)) == 0):
        return False
    if (np.count_nonzero((0 <= hint) & (hint < ns.num_choice)) == 0):
        return False

    return True

#}

iter: int = -1

while (True):

    iter += 1
    if (iter != 0):
        print()

    try:
        info_str: str = input('<number>... <num_hit> <num_blow>: ')
    except:
        print()
        break

    try:
        info: np.ndarray = np.array(list(map(lambda x: int(x), info_str.strip().split(' '))))
        if (not IsValidInput(info)):
            raise Exception()
    except:
        print('Invalid input.')
        continue

    colors: np.ndarray = info[:-2]
    num_hit: int = info[-2]
    num_blow: int = info[-1]

    for i, pattern in enumerate(possible_patterns[0]):
        possible_patterns[1][i] = False
        if (len(set(colors) & set(pattern)) == (num_blow + num_hit)):
            if (np.count_nonzero(colors == pattern) == num_hit):
                possible_patterns[1][i] = True

    #removes improper elements from `possible_patterns`
    tmp: np.ndarray = np.empty((2, np.count_nonzero(possible_patterns[1] == True)), dtype = object)
    tmp[0] = possible_patterns[0][possible_patterns[1] == True]
    tmp[1] = True
    possible_patterns = tmp

    num_possible_pattern: int = len(possible_patterns[0])
    print(f'Possible Patterns: {num_possible_pattern}')
    if (num_possible_pattern <= ns.num_printed_possible_pattern):
        for i in possible_patterns[0]:
            print(f' {i}')

    if (num_possible_pattern == 1):
        print()
        print('Solved.')
        break
    elif (num_possible_pattern == 0):
        print()
        print('No solution is found. It is suspected the inputs were not consistent.')
        break

# vim: spell:

