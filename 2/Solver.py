from copy import deepcopy
from Encoder import *
from time import clock

#definition of the  class with Clauses
class Clauses:
    def __init__(self):
        self.clause = []

#definition of the  class Guesses. This class is used when assigning values
class Guesses:
    def __init__(self):
        self.g = []
        self.guess = []
        self.dictguess = []
        self.clausesguess = []
        self.i = []


c = Clauses()

#function that reads the dimacs file and obtain the clauses and the number of variables
def readdimacs(filename):
    with open(filename, 'r') as f:

        for line in f:
            if line[0] == 'p':
                p = line.split()
                n_var = p[2]
            if line[0] != 'p' and line[0] != 'c':
                clause = line.split()
                clause = clause[:-1]
                c.clause.append(clause)
    return n_var


def solver(c, n_var):

    # creates a dictionary in which the keys are all variables and put None in all values
    varsdict = dict.fromkeys(range(1, int(n_var)+1))
    loop = True

    g = Guesses()
    g.g = []
    unity = []


    # sees if there are unit clauses, put them in a list and put the value of the variables contained in the clauses in
    # the dictionary. this is done before the dpll loop to improve the performance of the solver
    for i in range(len(c.clause)):
        if len(c.clause[i]) == 1:
            aux2 = 1
            var = c.clause[i][0]

            # check if the variable is denied in the clause
            if var[0] == '-':
                var = var[1:]
                aux2 = 0

            # search the variables in the dictionary and sees their values. if None or the same as in the clause
            # eliminates the clause and puts the value in the dictionary
            for key in varsdict.keys():
                if int(var) == key:
                    if varsdict[key] == aux2 or varsdict[key] == None:
                        if aux2 == 0:
                            varsdict[int(var)] = 0
                            unity.append(c.clause[i])
                            break

                        elif aux2 == 1:
                            varsdict[int(var)] = 1
                            unity.append(c.clause[i])
                            break

    # eliminate unit clauses
    for i in unity:
        c.clause.remove(i)



    # dpll loop
    while loop:
        listindex = []

        # eliminate the clauses that already have a true variable and the literals from clauses in which they have
        # different values than the ones in the dictionary
        for i in range(len(c.clause)):
            for var in c.clause[i]:
                breaking = False
                aux = 1
                # checks the sinal of the atom in the clauses
                if var[0] == '-':
                    var = var[1:]
                    aux = 0
                for key in varsdict.keys():
                    if key == int(var):
                        # if the var still hasn't been assigned, does nothing
                        if varsdict[key] == None:
                            break

                        # if the value is 0 both in the dictionary and in the clause puts in a list of clauses to erase
                        elif varsdict[key] == 0 and aux == 0:
                            c.clause[i] = ''
                            listindex.append(i)
                            breaking = True
                            break

                        # if the value is 1 both in the dictionary and in the clause puts in a list of clauses to erase
                        elif varsdict[key] == 1 and aux == 1:
                                c.clause[i] = ''
                                listindex.append(i)
                                breaking = True
                                break

                        # ckecks if the length of the clause is bigger than one
                        elif len(c.clause[i]) > 1:
                            # if the value is different in the dictionary and in the clause erase the literal from the
                            # clause
                            if varsdict[key] == 1 and aux == 0:
                                c.clause[i].remove('-' + str(key))
                                breaking = True
                                break
                            #if the value is different in the dictionary and in the clause erase the literal from the
                            # clause
                            elif varsdict[key] == 0 and aux == 1:
                                c.clause[i].remove(str(key))
                                breaking = True
                                break

                if breaking:
                    break
        aux3 = 0
        j = 1
        # removes from the clauses the clauses that are true
        for i in listindex:
            if aux3 == 1:
                i = i - j
                j += 1
            aux3 = 1
            c.clause.pop(i)


        # Checks if the length of the clauses list is 0. if it is it means that all the clauses are true which means
        # that the problem is solved
        if len(c.clause) == 0:
            return varsdict
        # if it isn´t continues the dpll
        else:
            loop = True


        # check if there is pure symbols and if there is eliminate the clauses and put the values in the dictionary
        # this part of the code is commented because it's vey inefficient.
        """
        breaking = False
        for key in varsdict.keys():
            if varsdict[key] == None:
                p = sum(x.count(str(key)) for x in c.clause)
                n = sum(x.count('-' + str(key)) for x in c.clause)

                if p > 0 and n == 0:
                    for i in range(len(c.clause)):
                        if key in c.clause[i]:
                            c.clause.pop(i)
                    varsdict[int(key)] = 1
                    breaking = True
                    break

                elif n > 0 and p == 0:
                    for i in range(len(c.clause)):
                        if key in c.clause[i]:
                            c.clause.pop(i)
                    varsdict[int(key)] = 0
                    breaking = True
                    break
        if breaking:
            continue
        """

        # checks if there are unit clauses. if there are eliminates them from the clauses list and puts the value of
        # the variables in the dictionary
        breaking = False

        for i in range(len(c.clause)):
            if len(c.clause[i]) == 1:
                aux2 = 1
                var = c.clause[i][0]
                # check if the atom is true or false in the unit clause
                if var[0] == '-':
                    var = var[1:]
                    aux2 = 0
                # put the calue of the atom in the dictionary and remove the clause
                for key in varsdict.keys():
                    breaking = False
                    if int(var) == key:
                        if varsdict[key] == aux2 or varsdict[key] == None:
                            if aux2 == 0:
                                varsdict[int(var)] = 0
                                c.clause.pop(i)
                                breaking = True
                                break

                            elif aux2 == 1:
                                varsdict[int(var)] = 1
                                c.clause.pop(i)
                                breaking = True
                                break
                if breaking:
                    break

        if breaking:
            continue



        # checks if there are keys in the dictionary with no value assigned. if there are gives an assign to one of them
        aux4 = 1
        for key in varsdict.keys():
            if varsdict[key] == None:
                aux4 = 0
                # assigns 0 to the variable
                varsdict[key] = 0
                if key not in g.g:
                    g.g.append(key)
                    g.i.append('1')
                g.guess.append(key)
                indexg = g.g.index(key)
                # saves the clauses and the dictionary at this time, to copy it back in the backtracking
                if g.i[indexg] == '1':
                    g.dictguess.append(deepcopy(varsdict))
                    g.clausesguess.append(deepcopy(c.clause))
                    g.i[indexg] = '0'
                break

        # checks if there are still variables that weren't backtracked and if there are still clauses in the list of
        # clauses. if there are the problem is unsatisfiable for this time and returns UNSAT
        if aux4 == 1:
            if g.guess == [] and len(c.clause) > 0:
                return 'UNSAT'
            # if there are still variables that were assigned and not backtracked calls the backtracking function
            else:
                [varsdict, g, c] = backtracking(varsdict, g, c)

# function that does the backtracking
def backtracking(varsdict, g, c):
    # searches in the dictionary the last variable that was assigned
    for key in varsdict.keys():
        if key == g.guess[-1]:
            # checks if the last assign of this variable was true or false and puts in the dictionary the inverse
            if varsdict[key] == 1:
                indexguess = g.guess.index(key)
                indexguess1 = g.g.index(key)
                # puts back the list of clauses and the dictionary that were when the variable was assigned
                for l in g.dictguess[indexguess1].keys():
                    if g.dictguess[indexguess1][l] == None:
                        varsdict[l] = None
                c.clause = deepcopy(g.clausesguess[indexguess1])
                varsdict[key] = 0
                # remove from the list of assigned variables the literal that was backtracked
                g.guess = g.guess[:indexguess]
                return [varsdict, g, c]
            else:
                indexguess = g.guess.index(key)
                indexguess1 = g.g.index(key)
                # puts back the list of clauses and the dictionary that were when the variable was assigned
                for l in g.dictguess[indexguess1].keys():
                    if g.dictguess[indexguess1][l] == None:
                        varsdict[l] = None
                c.clause = deepcopy(g.clausesguess[indexguess1])
                varsdict[key] = 1
                # remove from the list of assigned variables the literal that was backtracked
                g.guess = g.guess[:indexguess]
                return [varsdict, g, c]



# prints the result of the SAT problem
def print_result (varsdict, dictvaria, groundactions):
    # checks if the problem is unsatisfiable
    if varsdict == 'UNSAT':
        print('UNSAT')
    else:
        truevar = []
        listtoprint = []
        times = []
        # see what atoms are true
        for key in varsdict.keys():
            if varsdict[key] == 1:
                truevar.append(key)

        # checks if the atoms that are true are ground actions. if yes put in a list that will be printed
        for key in dictvaria.keys():
            for i in truevar:
                if int(i) == int(key):
                    t = dictvaria[key][-1]
                    atom = dictvaria[key][:-1]
                    for groundaction in groundactions:
                        if atom == groundaction:
                            listtoprint.append(atom)
                            times.append(t)

        taux = deepcopy(times)
        # put the groundactions in the order they are executed and print them in that order
        for l in range(len(taux)):
            tmin = (min(int(k) for k in taux))
            taux.pop(taux.index(str(tmin)))
            tminindex = times.index(str(tmin))
            print(listtoprint[tminindex])


