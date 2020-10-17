import datacontroller as dc
import matplotlib.pyplot as plt
import random as rnd
import collections
from operator import itemgetter
from datacontroller import data as data
from progress.spinner import Spinner
from progress.bar import Bar

#configuration settings
_mu = 50
_lambda = 100
_steps = 2000
_convergence = 0.000001
_crossover_rate = 0.1
_mutation_type = 0.001
_mutation_amount = 0.001
_mutation_power = 200

#Create the initial population according to the (parent)population size (_mu)
#and finding the intial evaluation function.
def createPopulation():
    global generation

    list_of_individuals = rnd.choices(list(dc.data.values()),k=_mu)
    generation = [(individual["ingredients"], evaluateFunction(individual["ingredients"])) for individual in list_of_individuals]
    return

#Wheel selection on parents, better parents have more chance to be having a child 
#then others. It selects two random indexes and then checks which fitness 
#that would be.
def parentSelection():
    global generation

    generation.sort(key=lambda x:x[1],reverse=True)
    max_fitness = sum(fit for _, fit in generation)
    random_fitness_p1 = rnd.random()
    random_fitness_p2 = rnd.random()
    index = 0

    while(random_fitness_p1 > 0 or random_fitness_p2 > 0):
        if(random_fitness_p1 > 0 and random_fitness_p1 - generation[index][1]/max_fitness < 0):
            r1 = generation[index]
        if(random_fitness_p2 > 0 and random_fitness_p2 - generation[index][1]/max_fitness < 0):
            r2 = generation[index]
        random_fitness_p1 -= generation[index][1]/max_fitness
        random_fitness_p2 -= generation[index][1]/max_fitness
        index += 1

    return (r1[0],r2[0])

#The crossover operator on two individuals holding only one child. It crossover on
#similiar on the bases component within the two ingredients.
def crossoverOperator(r1,r2):
    dict = defaultdict()

    for ingredient in r1:
        dict.setdefault(_ingredient["component"], []).append((1,ingredient))
    for ingredient in r2:
        dict.setdefault(_ingredient["component"], []).append((2,ingredient))

    crossovered = []

    for key,value in dict:
        for ingredient in value:
            if(ingredient[0] == 1 and rnd.random() > _crossover_rate):
               crossovered.append(ingredient[1])
            if(ingredient[0] == 2 and rnd.random() < _crossover_rate):
                crossovered.append(ingredient[1])
            
    return crossovered

#A subroutine that based on the subtype(property of the ingredient finds a ingredient 
#that shares that subtype. This can introduce also other new subtypes, if the new ingredient
#shares other subtypes.
def convertion(property_list,ingredient):
    property_idx = rnd.randint(0,len(property_list)-1)
    property = property_list[property_idx]

    list = dc.ingredient_subtype_dict[property]

    idx = rnd.randint(0,len(list)-1)

    return list[idx]

#The mutating operator that mutates a single individual. It individual has a chance
#to mutate the type of ingredient and the amount by a fixed max amount.
def mutationOperator(r1):
    for i in range(len(r1)):
        if(rnd.random() < _mutation_type):
            r1[i] = convertion(r1[i]["property"],r1[i])
        if(rnd.random() < _mutation_amount):
            r1[i]["amount"] = str(max([float(r1[i]["amount"]) + rnd.uniform(-_mutation_power,_mutation_power),0.1]))
    return r1

#The selection opeartor that picks the mu best individuals in a group of individuals.
#It selects the top _mu individuals in the list, based of the fitness function.
def selectionOperator(individuals):
    individuals.sort(key=lambda tuple:tuple[1],reverse=True)
    return individuals[0:_mu]

#The normalization operator to ensure that the recipies are correct and feasiable.
def normaliseOperator(r1):
    ingredient_dict = collections.defaultdict()

    for _ingredient in r1:
        ingredient_dict.setdefault(_ingredient["name"], []).append(_ingredient)

    new_ingredient_list = []
    for _,value in ingredient_dict.items():
        new_amount = 0 
        for ingredient_amount in value:
            new_amount += float(ingredient_amount["amount"])

        combined_ingredient = dc.ingredient(str(new_amount),value[0]["unit"],value[0]["name"],value[0]["component"],value[0]["property"])
        new_ingredient_list.append(combined_ingredient)

    r1 = new_ingredient_list
    return r1

#The evaluation function that determines how good the recipy is.
def evaluateFunction(r1):
    
    #for ingredient in r1["ingredients"]:


    return len(r1) + len(set([recipy["property"] for recipy in r1]))*10 + len(set([recipy["component"] for recipy in r1])) * 50

#A step in the genetic process.
def geneticStep():
    global generation

    children = []

    for i in range(_lambda):
        r1, r2 = parentSelection()
        r1 = crossoverOperator(r1,r2)
        r1 = mutationOperator(r1)
        r1 = normaliseOperator(r1)
        fr1 = evaluateFunction(r1)
        child = (r1,fr1)
        children.append(child)

    generation = selectionOperator(generation + children)
    return

def print_recipy(recipy):
    return


#The complete program
dc.loadData()

createPopulation()
currentsteps = 0
currentconvergence = 1
max_fitnesses = []
min_fitnesses = []

global best_found_solution
best_found_solution = "No recipy found",0

with Bar('Processing', max=_steps) as bar:
    for currentsteps in range(_steps): #and currentconvergence > _convergence):
        geneticStep()

        best = max(generation,key=itemgetter(1))
        worst = min(generation,key=itemgetter(1))

        currentconvergence = abs(best[1] - best_found_solution[1])

        if(best[1] > best_found_solution[1]):
            best_found_solution = best

        worstFit = worst[1]
        bestFit = best[1]
        min_fitnesses.append(worstFit)
        max_fitnesses.append(bestFit)
        bar.next()



for recipy in generation:
    print_recipy(recipy)

x  = range(currentsteps)
plt.plot(x, max_fitnesses, label="line L")
plt.fill_between(x, min_fitnesses, max_fitnesses, alpha=0.2)
plt.plot()

plt.xlabel("generation")
plt.ylabel("fitness")
plt.title("fitness over time")
plt.legend()
plt.show()