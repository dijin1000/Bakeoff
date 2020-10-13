import datacontroller as dc
import matplotlib.pyplot as plt

#example defining new recipy
if(False):
    dc.define_whole_new_recipy(
        "beef chilli",
        [
            [150,"g","minced beef"],
            [100,"g","onion"],
            [100,"ml","water"],
            [300,"g","tomato"],
            [5,"g","chilli powder"],
            [300,"g","red kidney beans"]
        ])
    dc.saveData()

#configuration settings
_mu = 10
_lambda = 10
_steps = 10000
_convergence = 0.000001
_crossoverRate = 0.01

#Create the initial population according to the (parent)population size (_mu)
def createPopulation():
    global generation

    generation = random.choices(data,k=_mu)
    return

#Wheel selection on parents, better parents have more chance to be having a child then others.
def parentSelection():
    global generation

    generation.sort(key=lambda x:x[1])

    max = sum(generation)[1]

    idx = random()
    idx2 = random()

    idx3 = 0

    while(idx > 0 or idx2 > 0):
        if(idx > 0 and idx - generation[idx3][1]/max < 0):
            r1 = generation[idx3]
        if(idx2 > 0 and idx2 - generation[idx3][1]/max < 0):
            r2 = generation[idx3]
        idx -= generation[idx3][1]/max
        idx2 -= generation[idx3][1]/max
        idx3 += 1

    return (r1,r2)

#The crossover operator on two individuals holding only one child.
def crossoverOperator(r1,r2):
    print("TODO")
    for i in range():
        if(random() > _crossoverRate):
            r1[i] = r2[i]
    return r1

#The mutating operator that mutates a single individual.
def mutationOperator(r1):
    print("TODO")
    for i in range():
        if(random() > _crossoverRate):
            r1[i] = r1[i] + 1
    return r1

#The selection opeartor that picks the mu best individuals in a group of individuals
def selectionOperator(individuals):
    individuals.sort(key=lambda x:x[1])
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
        r1, r2 = parentSelection(generation)
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
loadData()

createPopulation()

currentsteps = 0
currentconvergence = 1

max_fitnesses = []
min_fitnesses = []

global best_found_solution

while(currentsteps < _steps and currentconvergence < _convergence):
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