from sklearn import tree
from sklearn.model_selection import train_test_split
import pandas as pd
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




# Transforme la jouabilité en variables catégorique
def transformationJouabilite(jouabilites):
    targets = []
    for target in jouabilites:
        if target < 20:
            targets.append("E")
        elif target >= 20 and target < 40:
            targets.append("D")
        elif target >= 40 and target < 60:
            targets.append("C")
        elif target >= 60 and target < 80:
            targets.append("B")
        elif target >= 80:
            targets.append("A")
    return targets





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

    fields = ['Expected', 'Got']
    rows = []

    i = 0
    while i < len(targets_test) and i < len(targets_predicted):
        
        rows.append([targets_test[i], targets_predicted[i]])

        i = i + 1


    with open(fileName, 'w') as csvfile:  
        # creating a csv writer object  
        csvwriter = csv.writer(csvfile)  
            
        # writing the fields  
        csvwriter.writerow(fields)  
            
        # writing the data rows  
        csvwriter.writerows(rows)


















#---------------------------------------
# ARBRE DE DECISION POUR LES CREATURES
def decisionTreeCreatures():


    data_creatures = pd.read_csv('../data/clean/csv/creatures.csv')
    data_creatures = miseEnFormeFeatures(data_creatures)
    #Remplacement des NaN car ils posent pas mal de soucis
    data_creatures.fillna('aucun', inplace=True)


    features = data_creatures[data_creatures.columns.drop(["Jouabilite", ""])]


    #Transformation de la jouabilité pour qu'elle soit catégorique
    targets = transformationJouabilite(data_creatures["Jouabilite"])


    #Modification des variables catégoriques non adaptées pour l'arbre de décision

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


    #Création de l'arbre
    tree_model = tree.DecisionTreeClassifier()

    #Apprentissage
    tree_model.fit(features, targets)

    #Test du modèle
    target_prediction = tree_model.predict(features_test) 

    print("Prédiction pour les creatures terminée (arbre de décision)")

    printResults(targets_test, target_prediction, "../results/decisionTree/csv/decisionsTree_creatures.csv")

#---------------------------------------





















#---------------------------------------
# ARBRE DE DECISION POUR LES SORTS
def decisionTreeSorts():


    data_sorts = pd.read_csv('../data/clean/csv/spells.csv')
    data_sorts = miseEnFormeFeatures(data_sorts)
    #Remplacement des NaN car ils posent pas mal de soucis
    data_sorts.fillna('aucun', inplace=True)


    features = data_sorts[data_sorts.columns.drop(["Jouabilite", ""])]


    #Transformation de la jouabilité pour qu'elle soit catégorique
    targets = transformationJouabilite(data_sorts["Jouabilite"])


    #Modification des variables catégoriques non adaptées pour l'arbre de décision

    # Pour la classe, il n'y a que deux possibilité, on peut donc la transformer en Hunter? valant true si cardClass=hunter et false si cardClass=Paladin
    features.loc[features.cardClass == 'HUNTER', 'cardClass'] = True
    features.loc[features.cardClass == 'PALADIN', 'cardClass'] = False
    features = features.rename(columns=lambda x: x.replace("cardClass", "Hunter?"))


    #Gestion des variables catégoriques
    #On regroupe ensemble les catégories comprenant des variables identiques (comme les referencedTags par exemple)
    features = transformCategoricalVariables(features, ["referencedTags001", "referencedTags002"])
    features = transformCategoricalVariables(features, ["rarity"])
    features = transformCategoricalVariables(features, ["mechanics"])


    #On supprime la colonne "aucun" que l'on a dû créer
    features = supprimeSpecificColumns(features, ["aucun"])

    #Séparation variables de test et variables d'entrainement
    features_training, features_test, targets_training, targets_test = train_test_split(features, targets, test_size=1/5, random_state=0)


    #Création de l'arbre
    tree_model = tree.DecisionTreeClassifier()

    #Apprentissage
    tree_model.fit(features, targets)

    #Test du modèle
    target_prediction = tree_model.predict(features_test) 

    print("Prédiction pour les sorts terminée (arbre de décision)")

    printResults(targets_test, target_prediction, "../results/decisionTree/csv/decisionsTree_spells.csv")

#---------------------------------------

























#---------------------------------------
# ARBRE DE DECISION POUR LES ARMES
def decisionTreeWeapons():


    data_sorts = pd.read_csv('../data/clean/csv/weapons.csv')
    data_sorts = miseEnFormeFeatures(data_sorts)
    #Remplacement des NaN car ils posent pas mal de soucis
    data_sorts.fillna('aucun', inplace=True)


    features = data_sorts[data_sorts.columns.drop(["Jouabilite", ""])]


    #Transformation de la jouabilité pour qu'elle soit catégorique
    targets = transformationJouabilite(data_sorts["Jouabilite"])


    #Modification des variables catégoriques non adaptées pour l'arbre de décision

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


    #Création de l'arbre
    tree_model = tree.DecisionTreeClassifier()

    #Apprentissage
    tree_model.fit(features, targets)

    #Test du modèle
    target_prediction = tree_model.predict(features_test) 

    print("Prédiction pour les armes terminée (arbre de décision)")

    printResults(targets_test, target_prediction, "../results/decisionTree/csv/decisionsTree_weapons.csv")

#---------------------------------------
















# Arbre de décision pour les créatures
decisionTreeCreatures()

#Arbre de décision pour les sorts
decisionTreeSorts()

#Arbre de décision pour les armes
decisionTreeWeapons()