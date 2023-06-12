import subprocess
import os
from data.getValidAverSpectra import getValidAver, getSpectraforModeling
from notebook import run_notebook
import pandas as pd
import shutil
import numpy as np
from EvaluationTool import collection, evaluate
from QC_Model_Predictions.predict import predict_chems
from DSML87.split import split_data


def call(modeling_instructions, phone_number, evaluation_instructions):
    # """Get Repos"""
    # subprocess.run(f"{os.getcwd()}/repos.sh")

    # """
    # Get all averaged spectra
    # """
    # getValidAver()

    # os.makedirs("DSML87/inputFiles", exist_ok=True)
    # """Copy spc to DSML87"""
    # shutil.copy("outputFiles/spectraldata.csv",
    #             "DSML87/inputFiles/spectraldata.csv")

    # """
    # Make Predictions
    # """
    # predict_chems('QC_Model_Predictions/dl_models_all_chems_20210414/dl_v2.2_update_2022',
    #               'DSML87/outputFiles/preds', ['total_nitrogen', 'clay'], ['DLv2.2'], pd.read_csv('outputFiles/spectraldata.csv', index_col=0))
    # """Residual Outliers"""
    # run_notebook('DSML87', 'residual_outliers.ipynb')

    # """High Low Value Filter"""
    # run_notebook('DSML87', 'high_low_value_filter.ipynb')

    # """Mark Outliers"""
    # run_notebook('DSML87', 'Mark Outliers in Wetchem Data.ipynb')

    # """Get spectra for modelling"""
    # wetchem = pd.read_csv("DSML87/outputFiles/md_filtered.csv", index_col=0)
    # spc = getSpectraforModeling(wetchem.index)
    # wetchem = wetchem.loc[(wetchem.index.isin(spc.index))]
    # print(spc.index)
    # spc.to_csv('/home/tom/DSML125/DSML87/outputFiles/spc.csv')
    # wetchem.to_csv('/home/tom/DSML125/DSML87/outputFiles/wetchem.csv')
    """Train Test Split"""
    # subprocess.run(['bash', 'r_installation.sh'], check=True)
    # subprocess.run(['sudo','Rscript','/home/tom/DSML125/DSML87/splits.r'])

    # """Move Data to output files"""
    # subprocess.run
    # os.makedirs('outputFiles/spc', exist_ok=True)
    # os.makedirs('outputFiles/wetchem', exist_ok=True)
    # shutil.copy("./DSML87/outputFiles/spc.csv", "outputFiles/spc/spc.csv")
    # shutil.copy("./DSML87/outputFiles/wetchem.csv",
    #             "outputFiles/wetchem/wetchem.csv")
    # shutil.copytree("./DSML87/outputFiles/splits", "outputFiles/splits")
    """Zip data and push"""
    # shutil.copytree("outputFiles/spc", "MSSC_DVC/spc")
    # shutil.copytree("outputFiles/wetchem", "MSSC_DVC/wetchem")
    # shutil.copytree("outputFiles/splits", "MSSC_DVC/splits")
    # os.chdir(f"{os.getcwd()}/MSSC_DVC")
    # subprocess.run(['zip', '-r', 'data.zip', 'spc', 'wetchem', 'splits'], check=True)

    # subprocess.run(['bash', 'dvc_setup.sh'])
    # os.chdir("../")

    # """Run model optimization update"""

    chem_df = pd.read_csv(
        "inputFiles/2024-04-28_modeling-instructions_v2.5.csv")
    chemicals = chem_df['chemical'].values
    # os.chdir("dl")
    ips = ['157.245.71.196']
    # for chem in chemicals:
    #     command = ["bash", f"{os.getcwd()}/dl_spinner.sh", chem]
    #     ip = subprocess.check_output(command, universal_newlines=True)
    #     ip = ip.split('\n')[-2]
    #     ips.append(ip)

    # os.chdir("../")
    for ip, chemical in zip(ips, chemicals):
        print(ip)
        subprocess.run(
            ['bash', f"{os.getcwd()}/remotedatacollector.sh", "--server", ip, "--chemical", chemical])

        test_sample_codes = pd.read_csv(
            f"{os.getcwd()}/outputFiles/splits/{chemical}_test_sample_codes.csv")
        test_sample_codes = test_sample_codes['x'].values
        test_spc = pd.read_csv(
            f"{os.getcwd()}/outputFiles/spc/spc.csv", index_col=0)
        test_spc = test_spc.loc[test_spc.index.isin(test_sample_codes)]
        test_wetchem = pd.read_csv(
            f"{os.getcwd()}/outputFiles/wetchem/wetchem.csv", index_col=0)
        test_wetchem = test_wetchem.loc[test_wetchem.index.isin(
            test_sample_codes)]
        test_spc.to_csv(f"{os.getcwd()}/outputFiles/{chemical}_test_spc.csv")
        test_wetchem.to_csv(
            f"{os.getcwd()}/outputFiles/{chemical}_test_wetchem.csv")

        os.makedirs("outputFiles/predictions", exist_ok=True)
        evaluate.eval(
            [chemical],
            f"{os.getcwd()}/outputFiles/{chemical}_test_spc.csv",
            f"{os.getcwd()}/outputFiles/{chemical}_test_wetchem.csv",
            f"{os.getcwd()}/outputFiles/predictions",
            ['DLv2.6'],
            f"{os.getcwd()}/outputFiles/saved_model/saved_models",
            "outputFiles/predictions",
            "tom")

    # os.chdir(f"{os.getcwd()}/MSSC_DVC")
    # subprocess.run(['rm', '-rf', 'spc'])
    # subprocess.run(['rm', '-rf', 'wetchem'])
    # subprocess.run(['rm', '-rf', 'splits'])
    # os.chdir('../')


if __name__ == "__main__":
    call()
