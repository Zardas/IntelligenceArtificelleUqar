from sklearn.linear_model import LinearRegression
import json as js
import pandas as pd
import numpy as np

#weaponPaladinTraining = open('../data/clean/creatureTraining.json', encoding="utf-8")
#data = js.load(weaponPaladinTraining)




# Correction des derniers soucis du csv
# Des | et des _ ont été rajoutés lors du passage json->csv, il faut les supprimer
def miseEnFormeFeatures(data_toChange):
    data_toChange = data_toChange.rename(columns=lambda x: x.replace("|", "").replace("_", "").replace("-", ""))
    return data_toChange



# Fonction utilitaire
def supprimeSpecificColumns(data_toChange, featureList):
    for feature in featureList:
        data_toChange = data_toChange[data_toChange.columns.drop(feature)]
    return data_toChange




#Transforme une ou plusieurs colonnes avec des variables catégoriques en n colonnes où n est le nombre de catégories possibles
def transformCategoricalVariables(data_toChange, features):

    #On commence par obtenir la liste des différentes versions possibles de chaque variable catégorie
    possibleVariables = []
    for feature in features:
        for dat in data_toChange[feature]:
            if (not dat in possibleVariables):
                possibleVariables.append(dat)
    


    #On créer pour plus tard une matrice de Nombre_de_features*Nombre_de_cartes qui indique si la valeur de chaque feature pour chaque carte
    cardVariables = []
    for card in range(len(data[features[0]])):
        cardVariablesCurrent = [] 
        for numberOfFeatures in range(len(features)):
            cardVariablesCurrent.append(data[features[numberOfFeatures]][card])
        cardVariables.append(cardVariablesCurrent)



    #Puis, pour chaque variables on créer une colonne et on la remplit avec true ou false en fonction de si la feature correspond à cette variable
    for currentVariable in possibleVariables:
        var_array= []
        for dat in range(len(data_toChange[features[0]])):
            var_array.append(currentVariable in cardVariables[dat])
        #Puis on créer une nouvelle colonne à partir des données de ce tableau
        data_toChange[currentVariable] = var_array


    #On en profite pour supprimer les colonnes originelles
    data_toChange = supprimeSpecificColumns(data_toChange, features)

    return data_toChange
                









data = pd.read_csv('../data/clean/csv/creatureTest.csv')
data = miseEnFormeFeatures(data)
data.fillna('aucun', inplace=True)

#print(data)
features = data[data.columns.drop(["Jouabilite", ""])]
#features = data.loc[:, data.columns != "Jouabilite"]
target = data["Jouabilite"]










#Modification des variables catégoriques non adaptées pour la regression linéaire

# Pour la classe, il n'y a que deux possibilité, on peut donc la transformer en Hunter? valant true si cardClass=hunter et false si cardClass=Paladin

features['cardClass'] = features['cardClass'].replace(['HUNTER', 'PALADIN'],[True, False])
features = features.rename(columns=lambda x: x.replace("cardClass", "Hunter?"))



#Gestion des variables catégoriques

features = transformCategoricalVariables(features, ["mechanics001", "mechanics002"])
features = transformCategoricalVariables(features, ["rarity"])
features = transformCategoricalVariables(features, ["referencedTags"])
features = transformCategoricalVariables(features, ["race"])

#On supprime la colonne "aucun" que l'on a dû créer
features = supprimeSpecificColumns(features, ["aucun"])

print(features)

















#reg = LinearRegression(normalize=True)
#reg.fit(feature,target)


#https://larevueia.fr/regression-lineaire-fonctionnement-et-exemple-avec-python/
#https://www.askpython.com/python/examples/polynomial-regression-in-python