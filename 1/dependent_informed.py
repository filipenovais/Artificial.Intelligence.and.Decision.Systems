from read_and_print import * #import read_and_print
from independent_informed import * #imports this file so we can run the uniform cost to calculate the heuristic values

from queue import PriorityQueue #import the queue that we use


#this functions generate children an calculates the new cost of the new states and put them on the queue
def get_children(g, s, c, explored, cost_heur, path, state, queue, goal, cost, heuristics_cask_goal, heuristics_no_cask_goal):

    node, cask, stack_state = state.split(' ')#get the current node in the graph, the current cask that the CTS has
                                              # and the configuration of the stacks
    node_goal, cask_goal = goal.split(' ')#get the node goal in the graph and the cask goal from the goal string

    #runs the heuristics function
    g = heuristics_func(state, g, goal, heuristics_cask_goal, heuristics_no_cask_goal)

    # if the CTS has no cask
    if cask == '0':
        cask_to_load = 0 #that is no cask to load
        node_index = [g.id for g in g].index(node)#index of the node in the graph class

        # checks the neighbors of the node; calculates the new cost for the neighbors with heuristics and creates a new
        #  state for each neighbor; if that state was not explored yet, we add it to the queue
        for i in range(len(g[node_index].neighbors)):
            total_cost_heur = cost_heur + g[node_index].length[i] + float(g[node_index].heuristics[i])
            total_cost = cost + g[node_index].length[i]
            state = g[node_index].neighbors[i] + ' ' + str(cask_to_load) + ' ' + stack_state
            path_total = path + g[node_index].neighbors[i] + ';'
            if state not in explored:
                queue.put((total_cost_heur, state, path_total, total_cost))

    # if the CTS has a cask but it is not the cask goal
    if cask != '0' and cask != cask_goal:
        node_index = [g.id for g in g].index(node)#index of the node in the graph class

        # checks the neighbors of the node; calculates the new cost for the neighbors with heuristics and creates a new
        #  state for each neighbor; if that state was not explored yet, we add it to the queue
        for i in range(len(g[node_index].neighbors)):
            index_cask = [c.id for c in c].index(cask)
            total_cost_heur = cost_heur + g[node_index].length[i] * (1 + c[index_cask].weight) + g[node_index].heuristics[i]
            total_cost = cost + g[node_index].length[i] * (1 + c[index_cask].weight)
            path_total = path + g[node_index].neighbors[i] + ';'
            state = g[node_index].neighbors[i] + ' ' + cask + ' ' + stack_state
            if state not in explored:
                queue.put((total_cost_heur, state, path_total, total_cost))

    # Load action
    # checks if the CTS is in a stack and has no cask
    if node[0] == 'S' and cask == '0':
        aux = 1
        cask_to_load=''
        if aux == 1:
            stack_index = stack_state.index(node)#index of the stack in wich the CTS is
            #reads the stack state to find the cask to load in that stack
            x = stack_state[stack_index + 1:]
            if 'S' in x:
                next_stack_index = x.index('S')
                y = x[:next_stack_index]
                if 'C' in y:
                    cask_to_load = y[-2:]
            elif 'C' in x:
                cask_to_load = x[-2:]

        # if that is a cask to load we update the stack state, the state, the cost and if the state was not explored yet
        # put it in the queue
        if cask_to_load != '':
                stack_state = stack_state.replace(cask_to_load, '')
                state = node + ' ' +cask_to_load+ ' ' + stack_state
                index_cask = [c.id for c in c].index(cask_to_load)
                total_cost_heur = cost_heur + 1 + c[index_cask].weight
                total_cost = cost + 1 + c[index_cask].weight
                path_total = path + 'L' + cask_to_load + ';' + node + ';'
                if state not in explored:
                    queue.put((total_cost_heur, state, path_total, total_cost))


    # Unload Action
    # Checks if the CTS is in a stack, has a cask and this cask is not the cask goal
    if node[0] == 'S' and cask != '0' and cask != cask_goal:

        # reads the stack state to unload the current stack
        x = [s.id for s in s].index(node)

        stack_index = stack_state.index(node)
        v = stack_state[stack_index + 1:]
        if 'S' in v:
            next_stack_index = v.index('S')
            y = v[:next_stack_index]
            casks = []
        else:
            y = v
            casks = []
        for i in range(len(y)):
            if 'C' in y:
                index = y.index('C')
                casks.append(y[index] + y[index + 1])
                y = y[index + 2:]



        free_size_stack = s[x].size#checks the size of the current stack

        # checks if that is space for the cask in the current stack
        for j in casks:
            index_current_cask = [c.id for c in c].index(j)#index of the cask
            free_size_stack -= c[index_current_cask].length#subtract the length of the casks that are in the stack
            # to the size of the stack
        index_cask = [c.id for c in c].index(cask)
        if free_size_stack >= c[index_cask].length:  # verify stack space
            stack_index = stack_state.index(node)
            stack_index = stack_index+1
            x = stack_state[stack_index:]
            # update stack state
            if 'S' in x:
                next_stack_index = x.index('S')
                stack_index = next_stack_index + stack_index
                stack_state = stack_state[:stack_index] + cask + stack_state[stack_index:]
            else:
                stack_state = stack_state + cask

            # update the state, cost, and the path; if that state was not explored yet, we add it to the queue
            state = node + ' ' + '0' + ' ' + stack_state
            total_cost_heur = cost_heur + 1 + c[index_cask].weight
            total_cost = cost + 1 + c[index_cask].weight
            path_total = path + 'U' + cask + ';' + node +';'
            if state not in explored:
                queue.put((total_cost_heur, state, path_total, total_cost))

    # checks if the CTS has the cask goal
    if cask == cask_goal:
        node_index = [g.id for g in g].index(node)

        # checks the neighbors of the node; calculates the new cost for the neighbors with heuristics and creates a new
        #  state for each neighbor; if that state was not explored yet, we add it to the queue
        for i in range(len(g[node_index].neighbors)):
            index_cask = [c.id for c in c].index(cask)
            total_cost_heur = cost_heur + g[node_index].length[i] * (1 + c[index_cask].weight) + g[node_index].heuristics[i]
            total_cost = cost + g[node_index].length[i] * (1 + c[index_cask].weight)
            path_total = path + g[node_index].neighbors[i] + ';'
            state = g[node_index].neighbors[i] + ' ' + cask + ' ' + stack_state
            if state not in explored:
                queue.put((total_cost_heur, state, path_total, total_cost))


    return queue


#this function finds the stack where the cask goal is (stack pretended)
def searchcask(cask_pretended, s):
    stack_pretended=''
    for i in range(len([s.id for s in s])):
        for j in range(len(s[i].caskid)):
            if s[i].caskid[j] == cask_pretended:
                stack_pretended = s[i].id
                break

    return stack_pretended

#this function generates children so we can find the distance to the stack pretended and then the goal stack
def get_children_dist(g, explored, cost, node, queue):

    node_index = [g.id for g in g].index(node)
    for i in range(len(g[node_index].neighbors)):
        total_cost = cost + g[node_index].length[i]
        node = g[node_index].neighbors[i]
        if node not in explored:
            queue.put((total_cost, node))

    return [queue, g]


#this function searches the distance of every node in the graph to the stack where the cask goal is and put it in the
#list 'heuristics_no_cask_goal'
#also searches the distande of every node in the graph to the goal and put it in the list 'heuristics_cask_goal'
def search_dist(g, s, goal):
    #inicialize list
    heuristics_no_cask_goal = [[] for x in range(len([g.id for g in g]))]
    for i in range(len([g.id for g in g])):
        for j in range(len(g[i].neighbors)):
            explored = set()
            queue = PriorityQueue()
            queue.put((0, g[i].neighbors[j]))
            node_goal, cask_goal = goal.split(' ')
            stack_pretended = searchcask(cask_goal, s)

            node_goal = stack_pretended

            while queue:

                cost, node = queue.get()


                if node not in explored:
                    explored.add(node)

                    if node == node_goal:
                        break

                    [queue, g] = get_children_dist(g, explored, cost, node, queue)

            heuristics_no_cask_goal[i].append(cost/2)


    #inicialize list
    heuristics_cask_goal = [[] for x in range(len([g.id for g in g]))]
    for i in range(len([g.id for g in g])):
        for j in range(len(g[i].neighbors)):
            explored = set()
            queue = PriorityQueue()
            queue.put((0, g[i].id))
            node_goal = 'EXIT'

            while queue:

                cost, node = queue.get()

                if node not in explored:
                    explored.add(node)

                    if node == node_goal:
                        break

                    [queue, g] = get_children_dist(g, explored, cost, node, queue)


            heuristics_cask_goal[i].append(cost/2)


    return [heuristics_no_cask_goal, heuristics_cask_goal]

#heuristiscs funtion that changes if the cask of the CTS is the cask goal
def heuristics_func(state, g, goal, heuristics_cask_goal, heuristics_no_cask_goal):

    node, cask, stack_state = state.split(' ')
    node_index = [g.id for g in g].index(node)
    node_goal, cask_goal = goal.split(' ')

    if cask == cask_goal:
        num1 = 1
        num2 = 0
    else:
        num1 = 1
        num2 = 2
        g[node_index].heuristics = heuristics_no_cask_goal[node_index]

    for i in range(len(g[node_index].neighbors)):
        g[node_index].heuristics[i] = 0.1 * (num1 * heuristics_cask_goal[node_index][i] + num2 * heuristics_no_cask_goal[node_index][i])



    return g













