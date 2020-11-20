import pandas as pd
import json as js
import copy as cop
from csv import DictReader

#Les données ont été placés directement dans le fichier exercice3_data.csv
#training_data = pd.read_csv("../data/donneesInitiales.csv", delimiter=";")
#training_data = pd.read_csv("../data/cards.csv", delimiter=";")
#print(training_data)


weaponPaladinTraining = open('../data/cards_collectible.json', encoding="utf-8") 
data = js.load(weaponPaladinTraining)

#---------------------
#Fonctions utilitaires

#Fonction visualisant les data
def showData(data):
    i = 0
    for row in data:
        print(i, " : ", row)
        i = i + 1

#Fonction visualisant les hashmap
def showHashmap(hashmap):
    for key in hashmap:
        print(key, ": ", hashmap[key])

#Fonction vérifiant si un élément est dans un array
def isInArray(elem, givenArray):
    i = 0
    while (i+1) < len(givenArray) and elem != givenArray[i]:
        i = i + 1
    return elem == givenArray[i]

#Retourne une hashmap plaçant une feature en key et le reste en value
def transform_hashmap(data, key):
    newHashmap = {}
    for row in data:
        currentKey = row.get(key)
        row.pop(key, None)
        newHashmap[currentKey] = row
    return newHashmap

#---------------------




#Fonction établissant la liste des sets présents
def getPresentSets(cards_data):
    listOfPresentSets = []

    for row in cards_data:

        setDeLaLigne = row.get('set')
        aAjouter = True

        for presentSet in listOfPresentSets :
            if setDeLaLigne == presentSet:
                aAjouter = False
                break

        if aAjouter:
            listOfPresentSets.append(setDeLaLigne)
    return listOfPresentSets




#Suppression des sets qui ne nous interessent pas
def suppressionSets(data, unwantedSets):
    toRemove = []
    for row in data:
        if isInArray(row.get('set'), unwantedSets):
            toRemove.append(row)

    for elem in toRemove:
        data.remove(elem)
    return data


#Suppression des features qui ne nous interessent pas
def suppressionFeatures(data, unwantedFeatures):
    for row in data:
        for feature in unwantedFeatures:
            row.pop(feature, None)
    return data


#Fonction retournant uniquement avec la feature à l'état demandé
def allElementsWithFeature_X_egalTo_Y(data, feature, values):
    toRemove = []
    for row in data:
        #Vérification de si la feature désignée a une des valeurs désirées
        if not isInArray(row.get(feature), values):
            toRemove.append(row)

    for elem in toRemove:
        data.remove(elem)
    return data


#Fonction ajoutant une feature d'un hashmap à une autre hashmap
def addFeature(fromData, feature, toData, newName):
    for key in fromData:
        rowToChange = toData[key]
        rowToChange[newName] = fromData[key][feature]


#Fonction ajoutant la feature jouabilité au dataset finalData à partir du json jsonData
def addPercentage(jsonData, finalData):
    datasetPercentage = open(jsonData, encoding="utf-8")
    datasetPercentage = js.load(datasetPercentage)
    datasetPercentage = transform_hashmap(cop.deepcopy(datasetPercentage), 'Name')

    addFeature(datasetPercentage, "Percentage", finalData, "Jouabilite")


# 1 - Suppression des sets non désirés

#print("Sets présent initialement : ", getPresentSets(data))
data = suppressionSets(cop.deepcopy(data), ["TGT",
                              "BOOMSDAY",
                              "BRM",
                              "GANGS",
                              "HOF",
                              "NAXX",
                              "GILNEAS",
                              "GVG",
                              "HERO_SKINS",
                              "ICECROWN",
                              "KARA",
                              "LOE",
                              "LOOTAPALOOZA",
                              "OG",
                              "TROLL",
                              "UNGORO"])
#showData(data)
#print("Sets présent après suppression pour l'entrainement : ", getPresentSets(data))



# 2 - Suppression des classes non désirées
data = allElementsWithFeature_X_egalTo_Y(cop.deepcopy(data), "cardClass", ["PALADIN", "HUNTER"])


# 3 - Suppression des features non désirées
data = suppressionFeatures(cop.deepcopy(data), ["artist",
                                              "flavor",
                                              "collectible",
                                              "dbfId",
                                              "id",
                                              "text",
                                              "howToEarn",
                                              "howToEarnGolden",
                                              "classes",
                                              "multiClassGroup",
                                              "battlegroundsPremiumDbfId",
                                              "targetingArrowText",
                                              "elite",
                                              "techLevel",
                                              "faction"])







# 4 - Division en données d'entrainement et de test
# Les données de tests sont celles du dernier set (Scholomance), celles d'entrainement toutes les autres
#data_test = allElementsWithFeature_X_egalTo_Y(cop.deepcopy(data), "set", ["SCHOLOMANCE"])
#data = allElementsWithFeature_X_egalTo_Y(cop.deepcopy(data), "set", ["BLACK_TEMPLE", "CORE", "DEMON_HUNTER_INITIATE", "EXPERT1", "DALARAN", "DRAGONS", "ULDUM", "YEAR_OF_THE_DRAGON"])





# 5 - Division en trois datasets : creatures, sorts et armes
# Malheureusement, python passe les pramètres en reference, il faut donc faire une copie profonde avant de passer le dataset
# en paramètre, afin qu'il ne soit pas modifié dans la fonction
creatures = allElementsWithFeature_X_egalTo_Y(cop.deepcopy(data), "type", ["MINION"])
spells = allElementsWithFeature_X_egalTo_Y(cop.deepcopy(data), "type", ["SPELL"])
weapons = allElementsWithFeature_X_egalTo_Y(cop.deepcopy(data), "type", ["WEAPON"])

#creatureTest = allElementsWithFeature_X_egalTo_Y(cop.deepcopy(data_test), "type", ["MINION"])
#spellTest = allElementsWithFeature_X_egalTo_Y(cop.deepcopy(data_test), "type", ["SPELL"])
#weaponTest = allElementsWithFeature_X_egalTo_Y(cop.deepcopy(data_test), "type", ["WEAPON"])





# 6 - Suppression des dernières features non désirées (type que nous avions dû garder pour l'étape 3, et set que nous avions dû garder à l'étape 4)
creatures = suppressionFeatures(cop.deepcopy(creatures), ["type", "set"])
spells = suppressionFeatures(cop.deepcopy(spells), ["type", "set"])
weapons = suppressionFeatures(cop.deepcopy(weapons), ["type", "set"])

#creatureTest = suppressionFeatures(cop.deepcopy(creatureTest), ["type", "set"])
#spellTest = suppressionFeatures(cop.deepcopy(spellTest), ["type", "set"])
#weaponTest = suppressionFeatures(cop.deepcopy(weaponTest), ["type", "set"])


# 7 - Transformation en hashmap
creatures = transform_hashmap(cop.deepcopy(creatures), "name")
#creatureTest = transform_hashmap(cop.deepcopy(creatureTest), "name")

spells = transform_hashmap(cop.deepcopy(spells), "name")
#spellTest = transform_hashmap(cop.deepcopy(spellTest), "name")

weapons = transform_hashmap(cop.deepcopy(weapons), "name")
#weaponTest = transform_hashmap(cop.deepcopy(weaponTest), "name")

# 8 - Ajout de la jouabilité

addPercentage("../data/paladin/creatureTrainingPercentage.json", creatures)
addPercentage("../data/hunter/creatureTrainingPercentage.json", creatures)

addPercentage("../data/paladin/creatureTestPercentage.json", creatures)
addPercentage("../data/hunter/creatureTestPercentage.json", creatures)


addPercentage("../data/paladin/spellTrainingPercentage.json", spells)
addPercentage("../data/hunter/spellTrainingPercentage.json", spells)

addPercentage("../data/paladin/spellTestPercentage.json", spells)
addPercentage("../data/hunter/spellTestPercentage.json", spells)


addPercentage("../data/paladin/weaponTrainingPercentage.json", weapons)
addPercentage("../data/hunter/weaponTrainingPercentage.json", weapons)

addPercentage("../data/paladin/weaponTestPercentage.json", weapons)
addPercentage("../data/hunter/weaponTestPercentage.json", weapons)


# 9 - Enregistrement des 3 hashmap sous format json

with open('../data/clean/json/creatures.json', 'w') as json_file:
    js.dump(creatures, json_file)

#with open('../data/clean/creatureTest.json', 'w') as json_file:
    #js.dump(creatureTest, json_file)

with open('../data/clean/json/spells.json', 'w') as json_file:
    js.dump(spells, json_file)

#with open('../data/clean/spellTest.json', 'w') as json_file:
    #js.dump(spellTest, json_file)

with open('../data/clean/json/weapons.json', 'w') as json_file:
    js.dump(weapons, json_file)

#with open('../data/clean/weaponTest.json', 'w') as json_file:
    #js.dump(weaponTest, json_file)
    

