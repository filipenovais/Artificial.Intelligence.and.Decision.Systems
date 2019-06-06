#This file has the definition of the classes, reads the .dat file and prints the solution


#This class has all the cask information, such as, the cask id's and the casks length and weight
class Cask:
    def __init__(self, id, length, weight):
        self.id = id
        self.length = float(length)
        self.weight = float(weight)

#This class has all the stack information, such as, the stack id's, size and the id's of the casks that are stored
#in the stack
class Stack:
    def __init__(self, id, size, caskid):
        self.id = id
        self.size = int(size)
        self.caskid = caskid

#This class has all the information about the edges, such as, the nodes in the graph that are in that edge and
#the length from one to the other
class Edge:
    def __init__(self, node1, node2, length ):
        self.node1 = node1
        self.node2 = node2
        self.length = float(length)

#This class has the graph of the problem and the heuristics for the informed program
class Graph:
    def __init__(self, id, neighbors, length, heuristics):
        self.id = id
        self.neighbors = [neighbors]
        self.length = [float(length)]
        self.heuristics = [heuristics]

#This function reads the .dat file and fill in the classes
def readdat(filename):
    c=[]
    s=[]
    e=[]
    g=[]
    counte = 0
    countn = 0
    counts = 0
    initial_stack_state = ''
    with open(filename,'r') as f:
        for line in f:

            #In this if statement, we store the casks information
            if line[0] == 'C':
                l = line.rsplit(' ' , -1)
                l = [i.replace('\n', '') for i in l]
                c.append (Cask(l[0], l[1], l[2]))

            #In this if statement, we store the staks information
            elif line[0] == 'S':
                l = line.rsplit(' ', -1)
                l = [i.replace('\n', '') for i in l]
                s.append  (Stack(l[0], l[1], l[2:]))
                lstring = l[2:]
                makeitastring = ''.join(map(str, lstring))
                initial_stack_state += str(l[0]) + str(makeitastring)
                counts += 1

            #In this if statement, we store the edges information
            elif line[0] == 'E':
                line = line[2:]
                l = line.rsplit(' ', -1)
                l = [i.replace('\n', '') for i in l]
                e.append (Edge(l[0], l[1], l[2]))
                counte += 1

    # Here, we create the graph
    g.append (Graph(e[0].node1, e[0].node2, e[0].length, None))
    g.append (Graph(e[0].node2, e[0].node1, e[0].length, None))

    for i in range(1, counte):
        v=0
        v2=0

        for j in range(countn+2):

            if e[i].node1 == g[j].id:
                g[j].neighbors.append (e[i].node2)
                g[j].length.append (e[i].length)
                v = 1
            if e[i].node2 == g[j].id:
                g[j].neighbors.append (e[i].node1)
                g[j].length.append (e[i].length)
                v2=1

        if v != 1:
            g.append (Graph(e[i].node1, e[i].node2, e[i].length, None))
            countn = countn + 1
        if v2 != 1:
            g.append (Graph(e[i].node2, e[i].node1, e[i].length, None))
            countn = countn + 1


    return [c, s, g, initial_stack_state]


#This function prints the solusion as asked in the assignment
def print_sol(c, g, path, cost):

    path= 'EXIT;' + path
    path=path.split(';')
    loaded_index=0

    #this for statement reads the string 'path'
    for i in range(len(path)-2):

        #print Load action
        if "L" in path[i]:
            index_cask_to_load = [c.id for c in c].index(path[i][1:])
            load_cost  = 1 + c[index_cask_to_load].weight

            print('load %s %s %s' % (path[i][1:], path[i + 1], load_cost))
            loaded_index=1

        #print Unload action
        if "U" in path[i]:
            print('unload %s %s %s' % (path[i][1:], path[i + 1], load_cost))
            loaded_index = 0

        #print the Move action
        if "L" not in path[i] and "U" not in path[i] and "L" not in path[i+1] and "U" not in path[i+1]:
            node_index = [g.id for g in g].index(path[i])
            neighbor_index = g[node_index].neighbors.index(path[i+1])
            length_neighbor = g[node_index].length[neighbor_index]

            if loaded_index == 1:
                cost_neighbor = float(load_cost) * float(length_neighbor)
            else:
                cost_neighbor = length_neighbor

            print('move %s %s %f' % (path[i], path[i+1], cost_neighbor))

    print(cost) #print cost at the end



