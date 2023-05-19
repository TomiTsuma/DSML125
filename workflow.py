import subprocess
import os
from data.getValidAverSpectra import getValidAver, getSpectraforModeling
from notebook import run_notebook
import pandas as pd
import shutil


def call(modeling_instructions, phone_number, evaluation_instructions):
    """Get Repos"""
    # subprocess.run("bash repos.sh")

    """Copy spc to DSML87"""
    # shutil.copy("outputFiles/spectraldata.csv", "DSML87/inputFiles")

    """
    Get all averaged spectra
    """
    # getValidAver()

    """
    Make Predictions
    """
    # subprocess.run(
    #     f'python ./QC_Model_Predictions/predict.py --model-path ./QC_Model_Predictions/dl_models_all_chems_20210414/dl_v2.2_update_2022 --prediction-path ./DSML87/outputFiles/preds --chemicals total_nitrogen clay --model-versions DLv2.2 --spc ./outputFiles/spectraldata.csv')

    """Residual Outliers"""
    # run_notebook('DSML87', 'residual_outliers.ipynb')

    """High Low Value Filter"""
    # run_notebook('DSML87', 'high_low_value_filter.ipynb')

    # """Mark Outliers"""
    # run_notebook('DSML87', 'Mark Outliers in Wetchem Data.ipynb')

    """Get spectra for modelling"""
    # wetchem = pd.read_csv("DSML87/outputFiles/md_filtered.csv", index_col=0)
    # spc = getSpectraforModeling(wetchem.index)
    # wetchem = wetchem.loc[(wetchem.index.isin(spc.index))]
    # spc.to_csv('DSML87/outputFiles/spc.csv')
    # wetchem.to_csv('DSML87/outputFiles/wetchem.csv')

    # """Train Test Split"""
    # subprocess.run("python DSML87/split.py")

    """Move Data to output files"""
    # os.makedirs('outputFiles/spc', exist_ok=True)
    # os.makedirs('outputFiles/wetchem', exist_ok=True)
    # shutil.copy("./DSML87/outputFiles/spc.csv", "outputFiles/spc/spc.csv")
    # shutil.copy("./DSML87/outputFiles/wetchem.csv",
    #             "outputFiles/wetchem/wetchem.csv")
    # shutil.copytree("./DSML87/outputFiles/splits", "outputFiles/splits")

    # """Zip data and push"""
    # shutil.copytree("outputFiles/spc", "MSSC_DVC/spc")
    # shutil.copytree("outputFiles/wetchem", "MSSC_DVC/wetchem")
    # shutil.copytree("outputFiles/splits", "MSSC_DVC/splits")
    # os.chdir(f"{os.getcwd()}/MSSC_DVC")
    # subprocess.run('tar -cvf data.zip spc wetchem splits')

    # subprocess.run("bash dvc_setup.sh")
    # os.chdir("../")

    """DO Setups"""
    subprocess.run('Invoke-WebRequest https://github.com/digitalocean/doctl/releases/download/v1.94.0/doctl-1.94.0-windows-amd64.zip -OutFile ~\doctl-1.94.0-windows-amd64.zip')

    # """Run model optimization update"""
    # os.chdir("dl")
    # chem_df = pd.read_csv(
    #     "inputFiles/2024-04-28_modeling-instructions_v2.5.csv")
    # chemicals = chem_df['chemical'].values
    # subprocess.run("bash dl_spinner.sh")

    # """
    # Retrieve results
    # """


if __name__ == "__main__":
    call()
