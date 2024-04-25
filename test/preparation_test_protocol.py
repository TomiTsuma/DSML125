import pandas as pd
import os
from pathlib import Path
import shutil

def checkSpectraColumns():
    data = pd.read_csv("outputFiles/modeling_spectra.csv")
    data = data.T.head(1728).T

def checkSampleCodes():
    spc = pd.read_csv("outputFiles/modeling_spectra.csv", engine="c" , index_col=0)
    wetchem = pd.read_csv("../DS-ML87/outputFiles/md_filtered.csv", index_col=0)
    splits_dir = "../DS_ML94/outputFiles/splits"

    spc_2 =spc[(spc.index).isin(wetchem.index)]
    wetchem_2 = wetchem[(wetchem.index).isin(spc.index)]

    spc_2.to_csv("MSSC_DVC/spc/spc.csv")
    wetchem_2.to_csv("MSSC_DVC/wetchem/wetchem.csv")
    shutil.copy(splits_dir, "MSSC_DVC/splits")

