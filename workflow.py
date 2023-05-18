import subprocess
import os
from data.getValidAverSpectra import getValidAver, getSpectraforModeling
from notebook import run_notebook
import pandas as pd


def call():
    """Get Repos"""
    subprocess.run("bash repos.sh")

    """Get all averaged spectra"""
    getValidAver()

    """Residual Outliers"""
    run_notebook('DSML87', 'residual_outlier.ipynb')

    """High Low Value Filter"""
    run_notebook('DSML87', 'high_low_value_filter.ipynb')

    """Mark Outliers"""
    run_notebook('DSML87', 'Mark Outliers in Wetchem Data.ipynb')

    """Get spectra for modelling"""
    wetchem = pd.read_csv("DSML87/outputFiles/md_filtered.csv", index_col=0)
    spc = getSpectraforModeling(wetchem.index)
    wetchem = wetchem.loc[(wetchem.index.isin(spc.index))]
    spc.to_csv('DSML87/outputFiles/spc.csv')
    wetchem.to_csv('DSML87/outputFiles/wetchem.csv')

    """Train Test Split"""
    run_notebook('DSML87', 'Train Test Validation Split.ipynb')

    """Move Data to output files"""
    os.makedirs(['outputFiles/spc', 'outputFiles/wetchem'], exist_ok=True)
    subprocess.run("cp DSML87/outputFiles/spc.csv outputFiles/spc/spc.csv")
    subprocess.run(
        "cp DSML87/outputFiles/wetchem.csv outputFiles/wetchem/wetchem.csv")
    subprocess.run("cp -r DSML87/outputFiles/splits outputFiles")

    """Zip data and push"""
    subprocess.run("cp -r outputFiles/spc/ MSSC_DVC")
    subprocess.run("cp -r outputFiles/wetchem MSSC_DVC")
    subprocess.run("cp -r outputFiles/splits MSSC_DVC")
    os.chdir("MSSC_DVC")
    subprocess.run("zip -r data.zip spc wetchem splits")
    subprocess.run("bash dvc_setup.sh")
    os.chdir("../")

    """Run model optimization update"""
    os.chdir("dl")
    chem_df = pd.read_csv(
        "inputFiles/2024-04-28_modeling-instructions_v2.5.csv")
    chemicals = chem_df['chemical'].values
    subprocess.run("bash dl_spinner.sh")

    """
    Retrieve results
    """
