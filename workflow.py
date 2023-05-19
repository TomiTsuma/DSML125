import subprocess
import os
from data.getValidAverSpectra import getValidAver, getSpectraforModeling
from notebook import run_notebook
import pandas as pd
import shutil
import numpy as np


def call(modeling_instructions, phone_number, evaluation_instructions):
    """Get Repos"""
    # subprocess.run(f"{os.getcwd()}/repos.sh")

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

    """Run model optimization update"""

    chem_df = pd.read_csv(
        "inputFiles/2024-04-28_modeling-instructions_v2.5.csv")
    chemicals = chem_df['chemical'].values
    # os.chdir("dl")
    # for chem in chemicals:
    #     command = ["bash", f"{os.getcwd()}/dl_spinner.sh", chem]
    #     subprocess.run(command, check=True)
    #     break

    cmd = ['doctl', 'compute', 'droplet', 'list',
           '--format', "PublicIPv4", '--no-header']
    res = subprocess.run(cmd, check=True, capture_output=True, text=True)
    res = str(res.stdout).split('\n')[:len(chemicals)]
    print(f"The IP Addresses {(res)}++++++++ ")

    # """
    # Retrieve results
    # """


if __name__ == "__main__":
    call()
