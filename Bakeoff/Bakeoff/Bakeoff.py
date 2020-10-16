import datacontroller as dc
import matplotlib.pyplot as plt
import random as rnd
import collections
from datacontroller import data as data

#the types of ingredients we define
types = [
    "Sour",       #0
    "Water",      #1
    "Sweetness",  #2
    "Flour",      #3
    "Spice",      #4
    "Fluid",      #5
]

#example defining new recipy ( amount , unit, name, type as above ) 
if(True):
    dc.define_whole_new_recipy(
        "beef chilli",
        [
            [150,"g","minced beef",0],
            [100,"g","onion", 0],
            [100,"ml","water", 1],
            [300,"g","tomato", 2],
            [5,"g","chilli powder", 3],
            [300,"g","red kidney beans", 4]
        ])
    dc.saveData()

#configuration settings
_mu = 1
_lambda = 10
_steps = 10000
_convergence = 0.000001
_crossoverRate = 0.01

#Create the initial population according to the (parent)population size (_mu)
def createPopulation():
    global generation
    global dict 

    #generation = rnd.random.choices(data,k=_mu)
    generation = [(data["beef chilli"], 1)]


    zeta = [x for recipy in list(data.values()) for x in recipy["ingredients"]]

    dict = collections.defaultdict()

    for ingredient in zeta:
        dict.setdefault(ingredient["type"], []).append(ingredient) 

    return

#Wheel selection on parents, better parents have more chance to be having a child then others.
def parentSelection():
    global generation

    generation.sort(key=lambda x:x[1])

    max = sum(fit for _, fit in generation)

    idx = rnd.random()
    idx2 = rnd.random()

    idx3 = 0

    while(idx > 0 or idx2 > 0):
        if(idx > 0 and idx - generation[idx3][1]/max < 0):
            r1 = generation[idx3]
        if(idx2 > 0 and idx2 - generation[idx3][1]/max < 0):
            r2 = generation[idx3]
        idx -= generation[idx3][1]/max
        idx2 -= generation[idx3][1]/max
        idx3 += 1

    return (r1[0],r2[0])

#The crossover operator on two individuals holding only one child.
def crossoverOperator(r1,r2):
    print("TODO")

    r1_unique_idenitifier = list(set(map(lambda d: d['type'], r1["ingredients"])))
    r2_unique_idenitifier = list(set(map(lambda d: d['type'], r2["ingredients"])))

    unique_idenitifiers = r1_unique_idenitifier

    copy = r1["ingredients"]

    for idx in range(len(copy)):
        if(rnd.random() < _crossover):

            possibles = list(filter(lambda person: person['type'] == ingredient['type'], r2["ingredients"]))
            if(len(possibles) != 0):
                index = rnd.randint(0,len(possibles))
                copy[idx] = possibles[idx]

    return copy

#
def convertion(type,ingredient):
    global dict

    list = dict[type]
    list.remove(ingredient)

    idx = rnd.randint(0,len(list))

    return list[idx]

#The mutating operator that mutates a single individual.
def mutationOperator(r1):
    print("TODO")
    for i in range(len(r1["ingredients"])):
        if(rnd.random() < _mutation_type):
            r1["ingredients"][i] = convertion(r1["ingredients"][i]["type"])
        if(rnd.random() < _mutation_amount):
            r1["ingredients"][i]["amount"] += rnd.randint(-mutation_power,mutation_power)
    return r1

#The selection opeartor that picks the mu best individuals in a group of individuals
def selectionOperator(individuals):
    individuals.sort(key=lambda tuple:tuple[1])
    return individuals[0:_mu]

#The normalization operator to ensure that the recipies are correct and feasiable.
def normaliseOperator(r1):
    print("TODO")
    return r1

#The evaluation function that determines how good the recipy is.
def evaluateFunction(r1):
    print("TODO")
    return 1

#A step in the genetic process.
def geneticStep():
    global generation

    children = []

    for i in range(_lambda):
        r1, r2 = parentSelection()
        r1 = crossoverOperator(r1,r2)
        r1 = mutationOperator(r1)
        r1 = normalise(r1)
        fr1 = evaluateFunction(r1)
        child = (r1,fr1)
        children.append(child)

    generation = selectionOperator(generation,children)
    return

def printRecipy(recipy):
    print("TODO")
    return


#The complete program
dc.loadData()

createPopulation()

currentsteps = 0
currentconvergence = 1

max_fitnesses = []
min_fitnesses = []

global best_found_solution

while(currentsteps < _steps and currentconvergence > _convergence):
    geneticStep()

    best = max(generation)[1]
    if(best[1] > best_found_solution[1]):
        best_found_solution = best

    worstFit = min(generation)[1][1]
    bestFit = best[1]
    min_fitnesses.append(worstFit)
    max_fitnesses.append(bestFit)


print_recipy(best_found_solution[0])

x  = range(currentsteps)
plt.plot(x, max_fitnesses, label="line L")
plt.fill_between(x, min_fitnesses, max_fitnesses, alpha=0.2)
plt.plot()

plt.xlabel("generation")
plt.ylabel("fitness")
plt.title("fitness over time")
plt.legend()
plt.show()