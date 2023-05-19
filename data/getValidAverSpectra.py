import psycopg2
import pandas as pd
import ast
import numpy as np


def get_db_cursor():
    username = "doadmin"
    password = 'yzmodwh2oh16iks6'
    host = 'db-postgresql-cl1-do-user-2276924-0.db.ondigitalocean.com'
    port = 25060
    database = 'MandatoryMetadata'
    schema = 'historical'

    conn = psycopg2.connect(host=host, database=database,
                            user=username, password=password, port=port)
    cur = conn.cursor()
    cur.execute("SET search_path TO " + schema)

    return conn, cur


conn, cur = get_db_cursor()


def convertSpectra(df):
    _ = df.to_dict()
    df_2 = pd.DataFrame()
    df_2["sample_id"] = _['averaged_spectra'].keys()
    df_2 = df_2.set_index("sample_id")

    for sample in list(_['averaged_spectra'].keys()):
        spectra = _['averaged_spectra'][sample]
        # spectra = ast.literal_eval(spectra)
        key = list(spectra.keys())[0]
        spectra_list = spectra[key]
        for spectra_val, column in zip(spectra_list, np.arange(0, len(spectra_list)*2, 2)):
            df_2.loc[df_2.index == sample, column+522] = spectra_val

    return df_2


def getValidAver():
    conn, cur = get_db_cursor()
    spectra = pd.read_sql(
        "SELECT spectraldata.metadata_id, averaged_spectra, mandatorymetadata.sample_code  FROM spectraldata INNER JOIN mandatorymetadata ON mandatorymetadata.metadata_id = spectraldata.metadata_id WHERE (is_finalized=True AND (passed=True AND is_active=True AND averaged=True)) LIMIT 20", con=conn)
    conn.close()
    spectra = spectra[['sample_code', 'averaged_spectra']]
    spectra = spectra.set_index('sample_code')
    spectra = convertSpectra(spectra)
    spectra.to_csv("outputFiles/spectraldata.csv")

    return spectra


def getSpectraforModeling(sample_codes):
    spc = pd.read_csv("outputFiles/spectraldata.csv", index_col=0)
    spc = spc.loc[(spc.index.isin(sample_codes))]

    return spc
