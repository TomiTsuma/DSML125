from pathlib import Path
import pandas as pd
import numpy as np


def preparationCheck():
    path = Path("inputFiles")
    modeling_instructions = path.rglob("*_modeling-instructions_*.csv")
    file = None
    for f in (modeling_instructions):
        file = f

    return (file.name)


def checkPhone():
    try:
        df = pd.read_csv("inputFiles/phone_numbers.csv", index_col=0)
        print(df)
    except Exception as e:
        print(e)


def checkPrevModelSplits():
    patterns = ['train', 'test', 'valid']
    path = Path("./inputFiles/models in production")
    splits = []
    for pattern in patterns:
        for file in path.rglob(f'*_{pattern}_sample_codes.csv'):
            splits.append(file.name)


def checkPrevModel():
    modelingInstructions_df = pd.read_csv(
        "inputFiles/2024-04-28_modeling-instructions_v2.5.csv", index_col=0)
    modelingInstructions_df = modelingInstructions_df.loc[
        modelingInstructions_df.instructions == 'update']
    chemicals = list(modelingInstructions_df.index)
    if (len(chemicals) == 0):
        return False

    path_to_model = Path("../QC_Model_Predictions/")

    models = []
    for model in path_to_model.rglob("*/std/"):
        models.append(model.parent.name)
    chemicals.append('123')

    print(set(chemicals).issubset(models))


checkPrevModel()
