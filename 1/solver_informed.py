#imports
from independent_informed import *
from read_and_print import *
from dependent_informed import *
#import time
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

#runs heuristic function and uniforme cost search
[heuristics_cask_goal, heuristics_no_cask_goal] = search_dist(g, s, goal)
[path, cost_heur, cost, count] = search(g, s, c, start, goal, heuristics_cask_goal, heuristics_no_cask_goal)

#print the solution of the problem
print_sol(c, g, path, cost)

#print duration and the number of nodes explored
print('Nodes Explored -> %s\n ' % count)
#print("\nDuration\n------- %s seconds -------\n" % (time.time() - start_time))


