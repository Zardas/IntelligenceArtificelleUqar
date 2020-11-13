import pandas as pd
from csv import DictReader
import json as js
import copy as cop

#Les données de jouabilité
#training_data = pd.read_csv("../data/paladin/creatureTestPercentage.csv", delimiter="\t")




training_data_json = open('../data/paladin/weaponTrainingPercentage.json', encoding="utf-8") 
data = js.load(training_data_json)

def transform_hashmap(data, key):
    newHashmap = {}
    for row in data:
        currentKey = row.get(key)
        row.pop(key, None)
        newHashmap[currentKey] = row
    return newHashmap



t = transform_hashmap(cop.deepcopy(data), 'Name')
print(t)  