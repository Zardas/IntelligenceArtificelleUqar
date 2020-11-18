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





def transform(data_toChange, feature):

    #On commence par obtenir la liste des différentes versions possibles de chaque variable catégorie
    possibleVariables = []
    for dat in data_toChange[feature]:
        if (not dat in possibleVariables):
            possibleVariables.append(dat)
    
    #Puis, pour chaque variables on créer une colonne et on la remplit avec true ou false en fonction de si la feature correspond à cette variable
    for var in possibleVariables:
        var_array = []
        for dat in data_toChange[feature]:
            var_array.append(dat == var)
        #Pour chaque variable, on ajoute une colonne dont les valeurs valent True ou False en fonction de si l'élément à cette variable
        print(var_array)
        #data_toChange = data_toChange.assign(var = var_array)
        data_toChange[var] = var_array

    return data_toChange
                









data = pd.read_csv('../data/clean/csv/creatureTest.csv')
data = miseEnFormeFeatures(data)


features = data[data.columns.drop(["Jouabilite", ""])]
target = data["Jouabilite"]










#Modification des variables catégoriques non adaptées pour la regression linéaire

# Pour la classe, il n'y a que deux possibilité, on peut donc la transformer en Hunter? valant true si cardClass=hunter et false si cardClass=Paladin

features['cardClass'] = features['cardClass'].replace(['HUNTER', 'PALADIN'],[True, False])
features = features.rename(columns=lambda x: x.replace("cardClass", "Hunter?"))



#feature2 = features.assign(address = ['Delhi', 'Bangalore', 'Chennai', 'Patna', 'Delhi', 'Bangalore', 'Chennai', 'Patna', 'Delhi', 'Bangalore', 'Chennai', 'Patna', 'Cheh']) 


features = transform(features, "mechanics001")

print(features)















#reg = LinearRegression(normalize=True)
#reg.fit(feature,target)

#TODO : encode string
#https://stackoverflow.com/questions/34007308/linear-regression-analysis-with-string-categorical-features-variables#34008270

#https://larevueia.fr/regression-lineaire-fonctionnement-et-exemple-avec-python/
#https://www.askpython.com/python/examples/polynomial-regression-in-python