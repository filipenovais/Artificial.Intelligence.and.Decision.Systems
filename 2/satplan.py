from Encoder import *
from Solver import *
from time import clock
from sys import argv

filename = argv[1]

for h in range(0, 100):

    [sentence, countx, dictvaria, groundactions] = build_sentence(h, filename)

    dimacs(sentence, countx)
    n_var = readdimacs('dimacs.dat')
    result = solver(c, n_var)
    if result == 'UNSAT':
        continue
    print_result(result, dictvaria, groundactions)

    break