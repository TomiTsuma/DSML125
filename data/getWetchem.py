import pandas as pd
from pathlib import Path
import glob
import pyodbc
import numpy as np


def getWetchemLIMS(sample_codes=None, client=None, chemicals=None):
    
    chems = [
        'aluminium',
        'phosphorus',
        'ph',
        'exchangeable_acidity',
        'calcium',
        'magnesium',
        'sulphur',
        'sodium',
        'iron',
        'manganese',
        'boron',
        'copper',
        'zinc',
        'total_nitrogen',
        'potassium',
        'ec_salts',
        'organic_carbon', 'cec',
        'sand', 'silt', 'clay'
    ]
    conn_lims = pyodbc.connect("Driver={/opt/microsoft/msodbcsql18/lib64/libmsodbcsql-18.3.so.2.1};"
                            "TrustServerCertificate=yes;"
                            "Server=192.168.5.18\CROPNUT;"
                            "Database=cropnuts;"
                            "uid=thomasTsuma;pwd=GR^KX$uRe9#JwLc6")
    
    wet = pd.DataFrame()
    
    if(len(sample_codes) < 5000):
        count  = len(sample_codes)
        step=count
    elif(len(sample_codes) < 100000):
        count = len(sample_codes)
        step=5000
    else:
        count = 100000
        step=5000
    start = 0
    
    # not_null_clause = ""
    chemicals_clause = ""
    for c in chemicals:
        chemicals_clause = chemicals_clause + f"chemical_name LIKE '{c}' OR "
    # not_null_clause = " ".join(not_null_clause.split(" ")[:-2])
    chemicals_clause = " ".join(chemicals_clause.split(" ")[:-2])

    wet = pd.DataFrame()
    for i in np.arange(start, count, step):
        print("Fetching wetchem from {}".format(start))
        samples = [i for i in sample_codes][start:start+step]
        _ = pd.read_sql_query(f"SELECT sample_code, result, chemical_name from SampleResults where processed_date>'2023-03-03' AND ({chemicals_clause}) AND sample_code IN {str(samples).replace('[','(').replace(']',')')}  ORDER BY processed_date ASC", con=conn_lims)
        wet = pd.concat([wet, _], axis=0)
        start = start + step
        if (count-step) > 5000:
            step=5000
        else:
            step = count-step
    
    
    wet = pd.pivot_table(index='sample_code', values="result", columns="chemical_name", data=wet, aggfunc=max)
    wet = wet.reset_index()
    wet.columns = [i.lower().replace(" ","_").strip() for i in wet.columns]
    wet['sample_code'] = wet.sample_code.str.strip()
    # for c in chemicals:
    #     if(c not in wet.columns):
    #         raise Exception(f"{c} not in wetchem data")
    uncleaned_wetchem_df = wet.copy()
    uncleaned_wetchem_df = uncleaned_wetchem_df.rename(columns={"Unnamed: 0": "sample_code"})
    uncleaned_wetchem_df.set_index("sample_code")
    for column in uncleaned_wetchem_df.columns:
        if (column != 'sample_code'):
            vals = []
            for value in uncleaned_wetchem_df[column].values:
                if (value is not None):
                    value = str(value)
                    value = value.replace(">", "").replace(
                        "<", "").replace("...", "").strip()
                    try:
                        value = float(value)
                    except:
                        value = np.nan
                vals.append(value)
            uncleaned_wetchem_df[column] = vals

    wetchem_df = uncleaned_wetchem_df.copy(deep=True)
    wetchem_df.set_index("sample_code")

    return wetchem_df

def getWetchemData(latestModel, chemicals, operations, codes=None):
    chems = [
        'aluminium',
        'phosphorus',
        'ph',
        'exchangeable_acidity',
        'calcium',
        'magnesium',
        'sulphur',
        'sodium',
        'iron',
        'manganese',
        'boron',
        'copper',
        'zinc',
        'total_nitrogen',
        'potassium',
        'ec_salts',
        'organic_carbon', 'cec',
        'sand', 'silt', 'clay'
    ]
    path_to_splits = "/home/tom/DSML125/inputFiles/models_in_production"
    path_to_uncleaned_wetchem = "/home/tom/DSML125/inputFiles/uncleaned_wetchem.csv"
    train_samples = []
    test_samples = []
    valid_samples = []
    chems = [i for i in chems if i not in chemicals]

    for path in [x for x in Path(path_to_splits).glob("**/*_train_sample_codes.csv") if latestModel not in str(x)]:
        _ = pd.read_csv(str(path))
        col = ""
        for c in _.columns:
            if len([i for i in _[c] if "SA" in str(i)]) > 0:
                col = c
                break
        if (col == ""):
            print(str(path))
            continue

        train_samples = [*train_samples, *_[col].values]

    for path in [x for x in Path(path_to_splits).glob("**/*_test_sample_codes.csv") if latestModel not in str(x)]:
        _ = pd.read_csv(str(path))
        col = ""
        for c in _.columns:
            if len([i for i in _[c] if "SA" in str(i)]) > 0:
                col = c
                break
        if (col == ""):
            print(str(path))
            continue

        test_samples = [*test_samples, *_[col].values]

    for path in [x for x in Path(path_to_splits).glob("**/*_valid_sample_codes.csv") if latestModel not in str(x)]:
        _ = pd.read_csv(str(path))
        col = ""
        for c in _.columns:
            if len([i for i in _[c] if "SA" in str(i)]) > 0:
                col = c
                break
        if (col == ""):
            print(str(path))
            continue

        valid_samples = [*valid_samples, *_[col].values]

    uncleaned_wetchem = getWetchemLIMS(sample_codes=codes,chemicals=chemicals)

    df = pd.DataFrame()
    df['sample_code'] = uncleaned_wetchem.sample_code

    for i, j in zip(chemicals, operations):
        if (j == 'update'):
            _df = uncleaned_wetchem.loc[~(
                uncleaned_wetchem['sample_code'].isin([*train_samples, *test_samples, *valid_samples]))][['sample_code', i]]
            df = pd.merge(df, _df, on='sample_code', how="outer")
        else:
            _df = uncleaned_wetchem[['sample_code', i]]

            df = pd.merge(df, _df, on='sample_code', how="outer")
        

    # for i in chems:
    #     if (i.strip() in [x.strip() for x in chemicals]):
    #         print(i, "in chemicals")
    #         continue
    #     _df = uncleaned_wetchem[['sample_code', i]]

    #     df = pd.merge(df, _df, on='sample_code', how="outer")

    df.to_csv(
        path_to_uncleaned_wetchem)


