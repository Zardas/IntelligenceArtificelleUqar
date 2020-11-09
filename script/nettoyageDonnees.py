import pandas as pd
import json as js
import copy as cop

#Les données ont été placés directement dans le fichier exercice3_data.csv
#training_data = pd.read_csv("../data/donneesInitiales.csv", delimiter=";")
#training_data = pd.read_csv("../data/cards.csv", delimiter=";")
#print(training_data)


training_data_json = open('../data/cards_collectible.json', encoding="utf-8") 
data = js.load(training_data_json)

#---------------------
#Fonctions utilitaires

#Fonction visualisant les data
def showData(data):
    i = 0
    for row in data:
        print(i, " : ", row)
        i = i + 1

#Fonction vérifiant si un élément est dans un array
def isInArray(elem, givenArray):
    i = 0
    while (i+1) < len(givenArray) and elem != givenArray[i]:
        i = i + 1
    return elem == givenArray[i]

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
                                              "set",
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



# 4 - Division en trois datasets : creatures, sorts et armes
# Malheureusement, python passe les pramètres en reference, il faut donc faire une copie profonde avant de passer le dataset
# en paramètre, afin qu'il ne soit pas modifié dans la fonction
dataCreature = allElementsWithFeature_X_egalTo_Y(cop.deepcopy(data), "type", ["MINION"])
dataSpell = allElementsWithFeature_X_egalTo_Y(cop.deepcopy(data), "type", ["SPELL"])
dataWeapon = allElementsWithFeature_X_egalTo_Y(cop.deepcopy(data), "type", ["WEAPON"])


# 5 - Suppression de la dernière feature non désirée (type, que nous avions dû garder pour l'étape 4)
dataCreature = suppressionFeatures(cop.deepcopy(dataCreature), ["type"])
dataSpell = suppressionFeatures(cop.deepcopy(dataSpell), ["type"])
dataWeapon = suppressionFeatures(cop.deepcopy(dataWeapon), ["type"])

showData(dataSpell)