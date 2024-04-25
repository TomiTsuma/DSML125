import psycopg2
import pandas as pd
import ast
import numpy as np
from sqlalchemy import create_engine

def sqlalchemy_connection():
    username = "doadmin"
    password = 'yzmodwh2oh16iks6'
    host = 'db-postgresql-cl1-do-user-2276924-0.db.ondigitalocean.com'
    port = 25060
    database = 'MandatoryMetadata'
    schema = 'historical'
    engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}/{database}')

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
    print("Converting spectra")
    df_ = pd.DataFrame([i[[i for i in i.keys()][0]] for i in df['averaged_spectra'].values],columns = np.arange(522,3977,2))
    df_.index = df.index
    print("Spectra converted")
    return df_

def getSpectralCodes():
    query = f"SELECT DISTINCT mandatorymetadata.sample_code  FROM spectraldata INNER JOIN mandatorymetadata ON mandatorymetadata.metadata_id = spectraldata.metadata_id WHERE is_finalized=True AND passed=True AND is_active=True AND averaged=True"

    return pd.read_sql(query, con=conn)

def getValidAver(sample_codes, subset_count=None):
    conn, cur = get_db_cursor()
    spectra = pd.DataFrame(columns=['sample_code','averaged_spectra'])
    # count = len(sample_codes)
    if(len(sample_codes) < 5000):
        count  = len(sample_codes)
        step=count
    elif(len(sample_codes) < 70000):
        count = len(sample_codes)
        step=5000
    else:
        count = 100000
        step=5000
    start = 0

    for i in np.arange(start, count, step):
        
        print("Fetching spectra from {}".format(start))
        samples = [i for i in sample_codes][start:start+step]
        query = f"SELECT spectraldata.metadata_id, averaged_spectra, mandatorymetadata.sample_code  FROM spectraldata INNER JOIN mandatorymetadata ON mandatorymetadata.metadata_id = spectraldata.metadata_id WHERE is_finalized=True AND passed=True AND is_active=True AND averaged=True AND sample_code IN {str(samples).replace('[','(').replace(']',')')}"
        
        _ = pd.read_sql(query, con=conn)
        spectra = pd.concat([spectra, _], axis=0)
        start = start + step
        if (count-step) > 5000:
            step=5000
        else:
            step = count-step

    conn.close()
    spectra = spectra[['sample_code', 'averaged_spectra']]
    spectra = spectra.set_index('sample_code')
    spectra = convertSpectra(spectra)


    spectra.to_csv("/home/tom/DSML125/DSML87/outputFiles/spectraldata.csv")
    spectra.to_csv("/home/tom/DSML125/outputFiles/spectraldata.csv")

    return spectra


def getSpectraforModeling(sample_codes):
    spc = pd.read_csv(
        "/home/tom/DSML125/DSML87/outputFiles/spc_no_residual_outliers.csv", index_col=0, engine='c')
    spc = spc.loc[(spc.index.isin(sample_codes))]

    return spc


