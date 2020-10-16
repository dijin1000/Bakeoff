import json
from enum import Enum

global data
data = {}

#load the current data
def loadData():
    global data 
    with open('data.json', 'r') as readfile:
        data = json.loads(readfile.read())

#completly overwrite the previous data with the current data
def saveData():
    global data 
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile,indent=2,sort_keys=False,default=str)

#print the current data
def showData():
    global data 
    print(data)

#create a new recipy with ingredients
def define_whole_new_recipy(name,ingredients):
    define_new_recipy(name)
    for ingredient in ingredients:
        add_ingredients_to_recipy(name,ingredient[1],ingredient[2],ingredient[3],ingredient[0])

#create a new recipy with only a name
def define_new_recipy(name):
    data[name] = dataContainer()

#add ingredients to a already excisting recipy
def add_ingredients_to_recipy(name,ingredient_unit,ingredient_name,ingredient_type,ingredient_amount=1):
    data[name].add_ingredient(ingredient_unit,ingredient_name,ingredient_type,ingredient_amount)

#recipy container
class dataContainer(dict):
    def __init__(self):
        self["ingredients"] = list()
    
    def add_ingredient(self,ingredient_unit,ingredient_name,ingredient_type,ingredient_amount=1):
        self["ingredients"].append(ingredient(ingredient_amount,ingredient_unit,ingredient_name,ingredient_type))

#ingredients container
class ingredient(dict):
    def __init__(self,_amount,_unit,_name,_type):
        self["amount"] =_amount
        self["unit"] = _unit
        self["name"] = _name
        self["type"] = _type