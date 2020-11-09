import pandas as pd
import json as js

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
    i = 0
    toRemove = []
    for row in data:
        if isInArray(row.get('set'), unwantedSets):
            #print(i, " : ", row.get('name'), "(", row.get('set'), ")")
            toRemove.append(row)
        i = i + 1

    for elem in toRemove:
        data.remove(elem)
    return data


print("Sets présent initialement : ", getPresentSets(data))


data = suppressionSets(data, ["TGT",
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

print("Sets présent après suppression : ", getPresentSets(data))


