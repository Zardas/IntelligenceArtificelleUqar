from sklearn.linear_model import LinearRegression
import json as js
import pandas as pd
import numpy as np

#weaponPaladinTraining = open('../data/clean/creatureTraining.json', encoding="utf-8")
#data = js.load(weaponPaladinTraining)

data = pd.read_csv('../data/clean/csv/creatureTraining.csv')

# Correction des derniers soucis du csv
# Des | et des _ ont été rajoutés lors du passage json->csv, il faut les supprimer
def miseEnFormeFeatures(data_toChange):
    data_toChange = data_toChange.rename(columns=lambda x: x.replace("|", "").replace("_", "").replace("-", ""))
    return data_toChange


data = miseEnFormeFeatures(data)


feature = data[data.columns.drop(["Jouabilite", ""])]
target = data["Jouabilite"]

print(feature)



reg = LinearRegression(normalize=True)
reg.fit(feature,target)

#TODO : encode string

#https://larevueia.fr/regression-lineaire-fonctionnement-et-exemple-avec-python/
#https://www.askpython.com/python/examples/polynomial-regression-in-python