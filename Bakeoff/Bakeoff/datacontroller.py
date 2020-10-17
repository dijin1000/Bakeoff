import json
from enum import Enum
import collections

global data
data = {}

#load the current data
def loadData():
    global data 
    global ingredient_property_dict 
    global ingredient_subtype_dict

    ingredient_property_dict = collections.defaultdict()
    ingredient_subtype_dict = collections.defaultdict()

    with open('inspiring_set.json', 'r') as readfile:
        data = json.loads(readfile.read())

    ingredient_list = [ingredient for recipy in list(data.values()) for ingredient in recipy["ingredients"]]

    for ingredient in ingredient_list:
        ingredient_property_dict.setdefault(ingredient["component"], []).append(ingredient) 
        for subtype in ingredient["property"]:
            ingredient_subtype_dict.setdefault(subtype, []).append(ingredient) 

#completly overwrite the previous data with the current data
def saveData():
    global data 
    with open('inspiring_set.json', 'w') as outfile:
        json.dump(data, outfile,indent=2,sort_keys=False,default=str)

#create a new recipe with ingredients
def define_whole_new_recipe(name,ingredients):
    define_new_recipe(name)
    for ingredient in ingredients:
        add_ingredients_to_recipy(name,ingredient[1],ingredient[2],ingredient[3],ingredient[4],ingredient[0])

#create a new recipe with only a name
def define_new_recipe(name):
    data[name] = dataContainer()

#add ingredients to a already excisting recipy
def add_ingredients_to_recipy(name,ingredient_unit,ingredient_name,ingredient_type,ingredient_subtype,ingredient_amount=1):
    data[name].add_ingredient(ingredient_unit,ingredient_name,ingredient_type,ingredient_subtype, ingredient_amount)


#recipy container
class dataContainer(dict):
    def __init__(self):
        self["ingredients"] = list()
        self["servings"] = 0
    
    def add_ingredient(self,ingredient_unit,ingredient_name,ingredient_type,ingredient_subtype,ingredient_amount=1):
        self["ingredients"].append(ingredient(ingredient_amount,ingredient_unit,ingredient_name,ingredient_type,ingredient_subtype))

#ingredients container
class ingredient(dict):
    def __init__(self,_amount,_unit,_name,_type,_subtype):
        self["name"] =_name
        self["amount"] = _amount
        self["unit"] = _unit
        self["component"] = _type
        self["property"] = _subtype
