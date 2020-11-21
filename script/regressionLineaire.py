from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import tree
import json as js
import pandas as pd
import numpy as np
import csv





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
    for card in range(len(data_toChange[features[0]])):
        cardVariablesCurrent = [] 
        for numberOfFeatures in range(len(features)):
            cardVariablesCurrent.append(data_toChange[features[numberOfFeatures]][card])
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
                



# Ecrit les résultats de la prédiction du modèle dans fileName
def printResults(targets_test, targets_predicted, fileName):


    with open(fileName, 'w') as csvfile:

        # creating a csv writer object  
        csvwriter = csv.writer(csvfile)

        fields = ['Expected', 'Got', 'Difference', 'Predicted lower or higher']

        i = 0
        while i < len(targets_test) and i < len(targets_predicted):
            difference = abs(targets_test[i] - abs(targets_predicted[i]))
            if abs(targets_predicted[i]) > targets_test[i]:
                sign = "Predicted higher"
            else:
                sign = "Predicted lower"
            
            csvwriter.writerow([str(targets_test[i]), str(round(abs(targets_predicted[i]), 2)), str(round(difference, 2)), sign])
            i = i + 1















#---------------------------------------
# REGRESSION LINEAIRE POUR LES CREATURES

def regressionLineaireCreatures():

    data_creatures = pd.read_csv('../data/clean/csv/creatures.csv')
    data_creatures = miseEnFormeFeatures(data_creatures)
    #Remplacement des NaN car ils posent pas mal de soucis
    data_creatures.fillna('aucun', inplace=True)


    features = data_creatures[data_creatures.columns.drop(["Jouabilite", ""])]
    targets = data_creatures["Jouabilite"]


    #Modification des variables catégoriques non adaptées pour la regression linéaire

    # Pour la classe, il n'y a que deux possibilité, on peut donc la transformer en Hunter? valant true si cardClass=hunter et false si cardClass=Paladin
    features.loc[features.cardClass == 'HUNTER', 'cardClass'] = True
    features.loc[features.cardClass == 'PALADIN', 'cardClass'] = False
    features = features.rename(columns=lambda x: x.replace("cardClass", "Hunter?"))


    #Gestion des variables catégoriques
    #On regroupe ensemble les catégories comprenant des variables identiques (comme les mechanics par exemple)
    features = transformCategoricalVariables(features, ["mechanics001", "mechanics002", "mechanics003"])
    features = transformCategoricalVariables(features, ["rarity"])
    features = transformCategoricalVariables(features, ["referencedTags"])
    features = transformCategoricalVariables(features, ["race"])

    #On supprime la colonne "aucun" que l'on a dû créer
    features = supprimeSpecificColumns(features, ["aucun"])

    #Séparation variables de test et variables d'entrainement
    features_training, features_test, targets_training, targets_test = train_test_split(features, targets, test_size=1/5, random_state=0)

    #Entrainement du modèle
    reg = LinearRegression(normalize=True)
    reg.fit(features_training, targets_training)

    #Test du modèle
    target_prediction = reg.predict(features_test) 

    print("Prédiction pour les créatures terminée")

    printResults(targets_test.values, target_prediction, "../results/linearRegression/csv/linearRegression_creatures.csv")

#---------------------------------------






















#---------------------------------------
# REGRESSION LINEAIRE POUR LES SORTS

def regressionLineaireSpells():

    data_spells = pd.read_csv('../data/clean/csv/spells.csv')
    data_spells = miseEnFormeFeatures(data_spells)
    #Remplacement des NaN car ils posent pas mal de soucis
    data_spells.fillna('aucun', inplace=True)

    features = data_spells[data_spells.columns.drop(["Jouabilite", ""])]
    targets = data_spells["Jouabilite"]

    #Modification des variables catégoriques non adaptées pour la regression linéaire

    # Pour la classe, il n'y a que deux possibilité, on peut donc la transformer en Hunter? valant true si cardClass=hunter et false si cardClass=Paladin
    features.loc[features.cardClass == 'HUNTER', 'cardClass'] = True
    features.loc[features.cardClass == 'PALADIN', 'cardClass'] = False
    features = features.rename(columns=lambda x: x.replace("cardClass", "Hunter?"))


    #Gestion des variables catégoriques
    features = transformCategoricalVariables(features, ["referencedTags001", "referencedTags002"])
    features = transformCategoricalVariables(features, ["rarity"])
    features = transformCategoricalVariables(features, ["mechanics"])

    #On supprime la colonne "aucun" que l'on a dû créer
    features = supprimeSpecificColumns(features, ["aucun"])

    #Séparation variables de test et variables d'entrainement
    features_training, features_test, targets_training, targets_test = train_test_split(features, targets, test_size=1/5, random_state=0)

    #Entrainement du modèle
    reg = LinearRegression(normalize=True)
    reg.fit(features_training, targets_training)

    #Test du modèle
    target_prediction = reg.predict(features_test) 

    print("Prédiction pour les sorts terminée")

    printResults(targets_test.values, target_prediction, "../results/linearRegression/csv/linearRegression_spells.csv")

#---------------------------------------






















#---------------------------------------
# REGRESSION LINEAIRE POUR LES ARMES

def regressionLineaireWeapons():

    data_weapons = pd.read_csv('../data/clean/csv/weapons.csv')
    data_weapons = miseEnFormeFeatures(data_weapons)
    #Remplacement des NaN car ils posent pas mal de soucis
    data_weapons.fillna('aucun', inplace=True)

    features = data_weapons[data_weapons.columns.drop(["Jouabilite", ""])]
    targets = data_weapons["Jouabilite"]

    #Modification des variables catégoriques non adaptées pour la regression linéaire

    # Pour la classe, il n'y a que deux possibilité, on peut donc la transformer en Hunter? valant true si cardClass=hunter et false si cardClass=Paladin
    features.loc[features.cardClass == 'HUNTER', 'cardClass'] = True
    features.loc[features.cardClass == 'PALADIN', 'cardClass'] = False
    features = features.rename(columns=lambda x: x.replace("cardClass", "Hunter?"))


    #Gestion des variables catégoriques
    features = transformCategoricalVariables(features, ["referencedTags"])
    features = transformCategoricalVariables(features, ["rarity"])
    features = transformCategoricalVariables(features, ["mechanics"])

    #On supprime la colonne "aucun" que l'on a dû créer
    features = supprimeSpecificColumns(features, ["aucun"])

     #Séparation variables de test et variables d'entrainement
    features_training, features_test, targets_training, targets_test = train_test_split(features, targets, test_size=1/5, random_state=0)

    #Entrainement du modèle
    reg = LinearRegression(normalize=True)
    reg.fit(features_training, targets_training)

    #Test du modèle
    target_prediction = reg.predict(features_test) 

    print("Prédiction pour les armes terminée")

    printResults(targets_test.values, target_prediction, "../results/linearRegression/csv/linearRegression_weapons.csv")

#---------------------------------------




































#Creatures
regressionLineaireCreatures()

#Sorts
regressionLineaireSpells()

#Armes
regressionLineaireWeapons()



#https://larevueia.fr/regression-lineaire-fonctionnement-et-exemple-avec-python/
#https://www.askpython.com/python/examples/polynomial-regression-in-python
#https://www.askpython.com/python/examples/linear-regression-in-python
#https://www.youtube.com/watch?v=rw84t7QU2O0
