import json    # <-- could use YAML

global data
data = {}

#load the current data
def loadData():
    global data 
    data = json.load("data.txt")

#completly overwrite the previous data with the current data
def saveData():
    global data 
    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile,indent=2,sort_keys=False)

#print the current data
def showData():
    global data 
    print(data)

#create a new recipe with ingredients
def define_whole_new_recipe(name,ingredients):
    define_new_recipe(name)
    for ingredient in ingredients:
        add_ingredients_to_recipe(name,ingredient[1],ingredient[2],ingredient[0])

#create a new recipe with only a name
def define_new_recipe(name):
    data[name] = dataContainer()

#add ingredients to a already excisting recipe
def add_ingredients_to_recipe(name,ingredient_unit,ingredient_name,ingredient_amount=1):
    data[name].add_ingredient(ingredient_unit,ingredient_name,ingredient_amount)

#recipy container
class dataContainer(dict):
    def __init__(self):
        self["ingredients"] = list()
    
    def add_ingredient(self,ingredient_unit,ingredient_name,ingredient_amount=1):
        self["ingredients"].append(ingredient(ingredient_amount,ingredient_unit,ingredient_name))

#ingredients container
class ingredient(dict):
    def __init__(self,_amount,_unit,_name,_type,_subtype):
        self["amount"] =_amount
        self["unit"] = _unit
        self["name"] = _name
        self["type"] = _type
        self["sub-type"] = _subtype