import itertools
from copy import deepcopy


#definition of the  class with Actions, Preconditions and Effects
class Actions:

    def __init__(self, actions, preconditions, effects):
        self.actions = actions
        self.preconditions = preconditions
        self.effects = effects

#definition of the class to the encoder problem
class EncoderProblem:

    def __init__(self):
        self.initial = []
        self.goal = []
        self.consts = []
        self.actions = []
        self.groundactions = []
        self.hebrand = []
        self.relations = []

#funtion that builds sentence to use in the solver
def build_sentence(h, filename):
    ep = EncoderProblem() #start class enconderproblem
    a = []


    #function that fills the variables with the file information
    def readfile(filename):
        with open(filename, 'r') as f:

            #read all lines
            for line in f:
                #split lines and put it in the vector atoms
                atoms = line.split()
                if len(atoms) != 0:
                    #read first letter I
                    if atoms[0] == 'I':
                        for i in atoms[1:]:
                            ep.initial.append(i) #append the atoms in the ep.initial vector
                            find_relations_terms(i) #find the relationts terms in each atom

                    #read first letter G
                    elif atoms[0] == 'G':
                        for i in atoms[1:]:
                            ep.goal.append(i) #append the atoms in the ep.goal vector
                            find_relations_terms(i) #find the relationts terms in each atom

                    #read first letter A
                    elif atoms[0] == 'A':
                        index_arrow=atoms.index('->')
                        a.append(Actions(atoms[1],atoms[3:index_arrow],atoms[index_arrow+1:])) #append atoms in the actions class
                        list = atoms[1].split('(')
                        list[1] = list[1][:-1]
                        terms = list[1].split(',')
                        action = list[0] + str(len(terms))
                        ep.actions.append(action)  #append actions in ep.action
                        atoms.remove('->') #remove ->
                        atoms.remove(':') #remove :
                        for i in atoms[2:]:
                            find_relations_terms(i) #find the relationts terms in each atom

                    else:
                        print('error')
                        return

    # find the relation in each atom and save it in the vector ep.relations
    def find_relations_terms(word):
        aux=1
        aux1=1
        word = word[:-1]
        list = word.split('(')
        terms = list[1].split(',')
        #check for constants in the word and add to ep.consts if found
        for i in terms:
            if i[0].isupper():
                for j in ep.consts:
                    if i == j:
                        aux1=0
                if aux1 != 0:
                    ep.consts.append(i)
        list[0] = list[0] + str(len(terms))
        list[0] = list[0].replace('-', '')
        #get the relations and put them in ep.relations
        for j in ep.relations:
            if j == list[0]:
                aux = 0
        if aux != 0:
            ep.relations.append(list[0])

    readfile(filename)

    #create the hebrand base (ep.hebrand)
    for j in ep.relations:
            num=j[-1]
            perms = [','.join(p) for p in itertools.product(ep.consts, repeat=int(num))] #permutacion of the consts for each relation
            for l in perms:
                ep.hebrand.append(j[:-1]+ '(' + l + ')') # add parentheses
    #create the groundactions (ep.groundactions)
    for k in ep.actions:
            num = k[-1]
            perms = [','.join(p) for p in itertools.product(ep.consts, repeat=int(num))] #permutation of the consts for each groundactions
            for l in perms:
                ep.groundactions.append(k[:-1] + '(' + l + ')') # add parentheses


    #1
    sentence=[]
    dictvaria = {}
    t=0
    countx=1
    #initial state defined by a conjunction of ground actions
    for i in range(len(ep.hebrand)):
        if ep.hebrand[i] in ep.initial:
            dictvaria['%d' % countx] = ep.hebrand[i] + str(t)
            sentence.append(['%d' % countx]) #append to sentence
        #negate all the other states that are not in hebrand base
        else:
            dictvaria['%d' % countx] = ep.hebrand[i] + str(t)
            sentence.append(['-' + '%d' % countx])#append to sentence

        countx=countx+1 #count the number of keys in the dictionary


    # goal state defined by a conjuntction of ground actions
    for i in range(len(ep.goal)):
        aux=1
        goal = ep.goal[i]
        #check if is negative
        if goal[0] == '-':
            goal = goal[1:]
            aux=0
        #get goal from dictionary
        if goal + str(h) in dictvaria.values():
            for key in dictvaria.keys():
                if dictvaria[key] == goal + str(h):
                    x = key
                    break
        else:
            dictvaria['%d' % countx] = goal + str(h)
            x = '%d' % countx
            countx = countx + 1
        if aux==0:
            sentence.append(['-' + x]) # append to sentence if negative
        else:
            sentence.append([x]) # append to sentence if positive

    # put the values of the constants in the variables in the actions list1=list of actions, list2=list of
    # groundactions, list3=list of preconditions/effects
    def variables_to_constants(list1, list2, list3):

        list5 = []
        for i in range(len(list3)):
            #get index of parentheses
            ind1 = list3[i].index('(')
            ind2 = list3[i].index(')')
            list4 = list3[i][ind1 + 1:ind2].split(',') #list of preconditions/effects variables
            string1=''
            aux=1
            aux2=1
            #change the variables that are in the same place of each list
            for k in range(len(list4)):
                if any(x.isupper() for x in list4[k]):
                    aux2 = 0
                else:
                    aux2 = 1
                for l in range(len(list1)):
                    if list4[k] == list1[l] or aux2 == 0:
                        if list4[k] == list1[l]:
                            list4[k] = list2[l]
                        if len(list4) == 1:
                            list4[k] = list3[i][:ind1]+'('+list4[k]+')'
                            aux2 = 1
                        else:
                            string1 += list4[k] + ','
                            aux=0
                            aux2=1
            #append to list 5 and put the parentheses
            if aux == 0:
                list5.append(list3[i][:ind1] + '(' + string1[:-1] + ')')
                aux = 1
            else:
                list5.append(list4[k])


        return list5

    # append all the preconditions and effects in the sentence, for all the constants
    # go through all the ground actions for each action
    for  t in range(0, h):
        for i in range(len([a.actions for a in a])):
            openinda = a[i].actions.index('(')
            closeinda = a[i].actions.index(')')
            listact = a[i].actions[openinda + 1:closeinda].split(',')
            for j in range(len(ep.groundactions)):
                openindga = ep.groundactions[j].index('(')
                closeindga = ep.groundactions[j].index(')')
                listgroundact = ep.groundactions[j][openindga + 1:closeindga].split(',')
                if a[i].actions[:openinda] == ep.groundactions[j][:openindga]:
                    listapre = [] # list with the preconditions for that groundaction
                    listapre = [None] * len(a[i].preconditions)
                    listapre = list(a[i].preconditions)
                    listapre = variables_to_constants(listact, listgroundact, listapre) #substitute variables for constants

                    listeff = [] # list with the effects for that groundaction
                    listeff = [None] * len(a[i].effects)
                    listeff = list(a[i].effects)
                    listeff = variables_to_constants(listact, listgroundact, listeff) #substitute variables for constants

                    # check if action is in dictionary
                    if ep.groundactions[j] + str(t) in dictvaria.values():
                        for key in dictvaria.keys():
                            if dictvaria[key] == ep.groundactions[j] + str(t):
                                xaction = '-' + key #negate action
                                break
                    else: #if action is not in the dictionary values add new key and value to dictionary
                        dictvaria['%d' % countx] = ep.groundactions[j] + str(t)
                        xaction = '-' + '%d' % countx  #negate action
                        countx = countx + 1

                    # get groundactions of preconditions and put them in the dictionary
                    for l in range(len(listapre)):
                        aux = 1
                        pre = listapre[l]
                        if pre[0] == '-':
                            pre = pre[1:]
                            aux = 0
                        if pre + str(t) in dictvaria.values(): #if exists, get key of the dictionary
                            for key in dictvaria.keys():
                                if dictvaria[key] == pre + str(t):
                                    x = key
                                    break
                        else: #if doesnt exists add new key to dictionary
                            dictvaria['%d' % countx] = pre + str(t)
                            x = '%d' % countx
                            countx = countx + 1
                        if aux==0:
                            sentence.append((str(xaction) + ',' + '-' + str(x)).split(',')) # add signals and commas and append to sentence
                        else:
                            sentence.append((str(xaction) + ',' + str(x)).split(',')) # add commas and add to sentence

                    # get groundactions of preconditions and put them in the dictionary
                    for l in range(len(listeff)):
                        aux = 1
                        eff = listeff[l]
                        if eff[0] == '-':
                            eff = eff[1:]
                            aux=0
                        if eff + str(t+1) in dictvaria.values():#if exists, get key of the dictionary
                            for key in dictvaria.keys():
                                if dictvaria[key] == eff + str(t+1):
                                    x = key
                                    break
                        else:#if doesnt exists add new key to dictionary
                            dictvaria['%d' % countx] = eff + str(t+1)
                            x = '%d' % countx
                            countx = countx + 1
                        if aux==0:
                            sentence.append((str(xaction) + ',' + '-' + str(x)).split(','))# add signals and commas and append to sentence
                        else:
                            sentence.append((str(xaction) + ',' + str(x)).split(','))# add signals and commas and append to sentence


    #frame axions for each step and ground actions in the actions
    for  t in range(0, h):
        for i in range(len([a.actions for a in a])):
            openinda = a[i].actions.index('(')
            closeinda = a[i].actions.index(')')
            listact = a[i].actions[openinda + 1:closeinda].split(',')
            for j in range(len(ep.groundactions)):

                openindga = ep.groundactions[j].index('(')
                closeindga = ep.groundactions[j].index(')')
                listgroundact = ep.groundactions[j][openindga + 1:closeindga].split(',')
                if a[i].actions[:openinda] == ep.groundactions[j][:openindga]:
                    listapre = []
                    listapre = [None] * len(a[i].preconditions)
                    listapre = list(a[i].preconditions)
                    listapre = variables_to_constants(listact, listgroundact, listapre) #substitute variables for constants

                    listeff = []
                    listeff = [None] * len(a[i].effects)
                    listeff = list(a[i].effects)
                    listeff = variables_to_constants(listact, listgroundact, listeff) #substitute variables for constants

                    listeff = [s + str(t) for s in listeff] # add t to all the effects
                    groundactions = [s + str(t) for s in ep.groundactions] # add t to all the groundactions
                    if ep.groundactions[j] + str(t) in dictvaria.values():
                        for key in dictvaria.keys(): #get action if action exists in the dictionry
                            if dictvaria[key] == ep.groundactions[j] + str(t):
                                xaction = '-'+key
                                break
                    else:
                        dictvaria['%d' % countx] = ep.groundactions[j] + str(t)
                        xaction = '-' + '%d' % countx # add actions to the dictionary
                        countx = countx + 1

                    #make all the permutations of actions and groundactions that are not in listeff
                    copy = deepcopy(dictvaria)
                    listeffp = [s.replace('-', '') for s in listeff] #replace all the string - in the listeff list
                    for value in copy.values():
                        if value not in groundactions and value not in listeffp:
                            for key in copy.keys():
                                if copy[key] == value:
                                    x = key
                                    break
                            #check t in value
                            if value[-1] == str(t):
                                if value[:-1] + str(t + 1) in dictvaria.values(): #check if value + (t+1) is in the
                                    # dictionary and append in the sentence the expression pretended
                                    for key in dictvaria.keys():
                                        if dictvaria[key] == value[:-1] + str(t + 1):

                                            x2 = key
                                            sentence.append(('-' + str(x) + ',' + str(xaction) + ',' + str(x2)).split(','))
                                            sentence.append((str(x) + ',' + str(xaction) + ',' + '-' + str(x2)).split(','))
                                            break
                                else: #add value + t+1 in the dictionary and append in the sentence the expression pretended
                                    dictvaria['%d' % countx] = value[:-1] + str(t + 1)
                                    x2 = '%d' % countx
                                    countx = countx + 1
                                    sentence.append(('-' + str(x) + ',' + str(xaction) + ',' + str(x2)).split(','))
                                    sentence.append((str(x) + ',' + str(xaction) + ',' + '-' + str(x2)).split(','))

    #add all the actions in one list so we can have one action for each time step
    for t in range(0, h):
        groundaction = ''
        for j in range(len(ep.groundactions)):
            for key in dictvaria.keys():
                if dictvaria[key] == ep.groundactions[j] + str(t):
                    x = key
                    groundaction = str(groundaction) + ',' + str(x)
                    break


        groundaction = groundaction.split(',')
        del groundaction[0]
        sentence.append(groundaction) # append to sentence





    sentence = [[int(float(j)) for j in i] for i in sentence]

    return [sentence,countx, dictvaria, ep.groundactions]

#writes the sentence in a file called dimacacs.dat
def dimacs(sentence, countx):

    # create file to write
    f = open('dimacs.dat', 'w')

    #number of variables
    n_var = countx - 1
    #number of clauses in the sentence
    n_clauses = len(sentence)

    #write the first lines
    f.write(('p cnf \t %d \t %d \n' % (n_var, n_clauses)))
    f.write('c \n')

    write = ''
    #write every clause of the sentence in one line of the dimacs.dat file
    for cl in sentence:
        string = ''
        for var in cl:
            string = ' '.join((string, str(var)))

        write = ''.join((write, string[1:] + ' 0\n'))
    #write
    f.write(write)
    f.close()

