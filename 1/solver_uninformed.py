#imports
from independent_uninformed import *
from read_and_print import *
from dependent_uninformed import *
import time
from sys import argv

#check execution time
#start_time = time.time()

#reads argumments from the terminal/cmd
filename = argv[1]
caskgoal = argv[2]

#read .dat file
[c, s, g, initial_stack_state] = readdat(filename)

#define the start and end goal
start = 'EXIT'+' 0 '+ initial_stack_state
goal = 'EXIT ' + caskgoal

#runs uniforme cost search
[path, cost, count] = search(g, s, c, start, goal)

#print the solution of the problem
print_sol(c, g, path, cost)

#print duration and the number of nodes explored
print('Nodes Explored -> %s\n ' % count)
#print("\nDuration\n------- %s seconds -------\n" % (time.time() - start_time))

