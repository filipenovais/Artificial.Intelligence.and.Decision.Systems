#This file has the independent function that runs the uniform cost algorithm

from read_and_print import * #import this file so we can use the classe lists created in that file
from dependent_uninformed import get_children   #import get_children function

from queue import PriorityQueue #import the queue that we use


# this function runs the uniform cost search
def search(g, s, c, start, goal):
    path='' #initialize the path string
    explored = set() #initialize the set that will contain the explored states
    queue = PriorityQueue()
    queue.put((0, start, path)) #initialize queue
    count = 0 #initialize the nodes counter

    #this while runs until that is nothing in the queue or reaches a break/return
    while queue:

        cost, state, path = queue.get() #queue.get() picks the state with the minimum cost and pops it out of the queue

        #this if statement is to check if the state in wich we are already was explored
        if state not in explored:
            count += 1  #count the nodes that were explored
            explored.add(state) #add to the explored set a state

            #this if statement checks if the state that we are in is the goal state
            if state[0:7] == goal:
                return [path, cost, count] #return values

            #generate children from the current state
            [queue, g] = get_children(g, s, c, explored, cost, path, state, queue, goal)



