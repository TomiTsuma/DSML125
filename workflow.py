import subprocess
import os
from data.getValidAverSpectra import getValidAver, getSpectraforModeling
from data.retrieve_prev_splits import retrieve_splits
from notebook import run_notebook
import pandas as pd
import shutil
import numpy as np
from EvaluationTool import collection, evaluate
from QC_Model_Predictions.predict import predict_chems
from DSML87.split import split_data
import logging


def call(modeling_instructions, phone_number, evaluation_instructions, version):
    logging.basicConfig(filename='training.log', level=logging.INFO)

    modelingInstructions = pd.read_csv(modeling_instructions)
    chemicals = modelingInstructions['chemical']
    instructions = modelingInstructions['instructions']

    phone_numbers = pd.read_csv(phone_number)
    phone_numbers = phone_numbers['phone']

    evaluationInstructions = pd.read_csv(evaluation_instructions)
    dataUsed = evaluationInstructions['data_used'].values
    modelsUsed = evaluationInstructions['models_used'].values

    dataAvailable = [float(str(i).replace("v", "")) for i in os.listdir(
        "/home/tom/DSML125/inputFiles/models in production") if "v" in i]
    dataUsed = [str(i).replace("v", "") for i in dataUsed]
    dataUsed = [str(i).replace(
        "past", "-".join([str(j) for j in dataAvailable if (len(i.split("-")) > 1 and float(j) < float(i.split("-")[1]))])) for i in dataUsed]
    dataUsed = [[f"v{j}" for j in i.split("-")] for i in dataUsed]

    # Ensure that the versions of data and models specified are present. Otherwise make sure to break
    print(dataUsed)
    print([i.split("-") for i in modelsUsed])
    dataAvailable = [i for i in os.listdir('/home/tom/DSML125/models in production')]
    modelsAvailable = [i for i in os.listdir('/home/tom/DSML125/QC_Model_Predictions/dl_models_all_chems_20210414')]
    print(dataAvailable)
    print(modelsAvailable)


    dataUnavailable = [version for version in [i for j in dataUsed for i in j] if version not in dataAvailable]
    modelsUnavailable = [version for version in [i for j in [i.split("-") for i in modelsUsed] for i in j] if version not in modelsAvailable]

    print(dataUnavailable)
    print(modelsUnavailable)
    if(len(dataUnavailable) > 0):
        for phone in phone_numbers:
            print(phone)
            subprocess.run(["python", "sms.py", "--phone", f"{phone}", "--message", f"The following data is unavailable {str(','.join(dataUnavailable))}"])
        return
    if(len(modelsUnavailable) > 0):
        for phone in phone_numbers:
            subprocess.run(["python", "sms.py", "--phone", f"{phone}", "--message", f"The following models are unavailable {str(','.join(modelsUnavailable))}"])
        return
    return
    logging.info(f"Data Used", str(dataUsed))

    """Preliminary Actions"""
    os.chdir(f"{os.getcwd()}/MSSC_DVC")
    subprocess.run(['rm', '-rf', 'spc'])
    subprocess.run(['rm', '-rf', 'wetchem'])
    subprocess.run(['rm', '-rf', 'splits'])
    subprocess.run(['rm', 'data.zip'])
    os.chdir(f'/home/tom/DSML125')
    os.chdir(f"{os.getcwd()}/outputFiles")
    subprocess.run(['rm', '-rf', 'spc'])
    subprocess.run(['rm', '-rf', 'wetchem'])
    subprocess.run(['rm', '-rf', 'splits'])
    subprocess.run(['rm', '-rf', 'predictions'])
    os.chdir(f'/home/tom/DSML125')
    os.chdir(f"{os.getcwd()}/DSML87")
    subprocess.run(['rm', '-rf', 'outputFiles/splits'])
    subprocess.run(['rm', '-rf', 'outputFiles/wetchem'])
    subprocess.run(['rm', '-rf', 'outputFiles/spc'])
    os.chdir(f'/home/tom/DSML125')
    """Get Repos"""
    # subprocess.run(f"{os.getcwd()}/repos.sh")

    # """Connect to vpn"""
    # subprocess.run(["bash", "vpn_con.sh"])

    # """Get previous splits"""
    # retrieve_splits()
    # """
    # Get all averaged spectra
    # """
    # # getValidAver()

    # os.makedirs("DSML87/inputFiles", exist_ok=True)
    # """Copy spc to DSML87"""
    # shutil.copy("outputFiles/spectraldata.csv",
    #             "DSML87/inputFiles/spectraldata.csv")

    # """
    # Make Predictions
    # """
    # predict_chems('QC_Model_Predictions/dl_models_all_chems_20210414/v2.2',
    #               'DSML87/outputFiles/preds', chemicals, ['v2.2'], pd.read_csv('outputFiles/spectraldata.csv', index_col=0))

    # os.makedirs("DSML87/outputFiles/splits", exist_ok=True)
    # os.makedirs("DSML87/outputFiles/rds", exist_ok=True)
    # """Residual Outliers"""
    # run_notebook('DSML87', 'residual_outliers.ipynb')

    # """High Low Value Filter"""
    # run_notebook('DSML87', 'high_low_value_filter.ipynb')

    # """Mark Outliers"""
    # # run_notebook('DSML87', 'Mark Outliers in Wetchem Data.ipynb')

    # """Get spectra for modelling"""
    # wetchem = pd.read_csv("DSML87/outputFiles/md_filtered.csv", index_col=0)
    # spc = getSpectraforModeling(wetchem.index)
    # wetchem = wetchem.loc[(wetchem.index.isin(spc.index))]
    # if (len(spc.index) < 1):
    #     logging.error(f"Not enough spectra for modelling")
    # spc.to_csv('/home/tom/DSML125/DSML87/outputFiles/spc.csv')
    # wetchem.to_csv('/home/tom/DSML125/DSML87/outputFiles/wetchem.csv')
    # """Train Test Split"""
    # # subprocess.run(['bash', 'r_installation.sh'], check=True)
    # subprocess.run(['sudo', 'Rscript', '/home/tom/DSML125/DSML87/splits.r'])

    """Move Data to output files"""
    os.makedirs('outputFiles/spc', exist_ok=True)
    os.makedirs('outputFiles/wetchem', exist_ok=True)
    shutil.copy("./DSML87/outputFiles/spc.csv", "outputFiles/spc/spc.csv")
    shutil.copy("./DSML87/outputFiles/wetchem.csv",
                "outputFiles/wetchem/wetchem.csv")

    # os.makedirs(f"inputFiles/models in production/{version}", exist_ok=True)
    # try:
    #     shutil.copytree("./DSML87/outputFiles/splits",
    #                     f"inputFiles/models in production/{version}/splits")
    # except Exception as e:
    #     logging.info(e)
    # try:
    #     shutil.copytree("./DSML87/outputFiles/splits", "outputFiles/splits")
    # except Exception as e:
    #     logging.info(e)
    # """Zip data and push"""
    # try:
    #     shutil.copytree("outputFiles/spc", "MSSC_DVC/spc")
    # except Exception as e:
    #     logging.info(e)

    # try:
    #     shutil.copytree("outputFiles/wetchem", "MSSC_DVC/wetchem")
    # except Exception as e:
    #     logging.info(e)

    # try:
    #     shutil.copytree("outputFiles/splits", "MSSC_DVC/splits")
    # except Exception as e:
    #     logging.info(e)
    # os.chdir(f"{os.getcwd()}/MSSC_DVC")
    # subprocess.run(['zip', '-r', 'data.zip', 'spc',
    #                'wetchem', 'splits'], check=True)

    # subprocess.run(['bash', 'dvc_setup.sh'])
    # os.chdir("../")

    # """Run model optimization update"""

    # chem_df = pd.read_csv(
    #     f"{modeling_instructions}")
    # chemicals = chem_df['chemical'].values
    # os.chdir("dl")
    # ips = ['64.227.75.34']
    # for chem in chemicals:
    #     command = ["bash", f"{os.getcwd()}/dl_spinner.sh", chem]
    #     ip = subprocess.check_output(command, universal_newlines=True)
    #     ip = ip.split('\n')[-2]
    #     ips.append(ip)

    # os.chdir("../")

    # for ip, chemical in zip(ips, chemicals):
    #     subprocess.run(["bash", "remotedatacollector.sh",
    #                    "--chemical", chemical, "--server", ip, "--version", version])

    os.makedirs("outputFiles/predictions", exist_ok=True)
    for data, models in zip(dataUsed, [str(i).split("-") for i in modelsUsed]):
        for dataVersion in data:
            for chemical in chemicals:
                print(chemical)
                try:
                    test_sample_codes = pd.read_csv(
                        f"{os.getcwd()}/inputFiles/models in production/{dataVersion}/splits/{chemical}_test_sample_codes.csv")
                except Exception as e:
                    logging.error(e)
                    break

                if ("x" not in test_sample_codes.columns):
                    continue
                test_spc = pd.read_csv(
                    f"{os.getcwd()}/outputFiles/spc/spc.csv", index_col=0)
                test_spc = test_spc.loc[test_spc.index.isin(
                    test_sample_codes['x'])]
                test_wetchem = pd.read_csv(
                    f"{os.getcwd()}/outputFiles/wetchem/wetchem.csv", index_col=0)
                test_wetchem = test_wetchem.loc[test_wetchem.index.isin(
                    test_sample_codes['x'])]
                test_spc.to_csv(
                    f"{os.getcwd()}/outputFiles/{chemical}_test_spc.csv")
                test_wetchem.to_csv(
                    f"{os.getcwd()}/outputFiles/{chemical}_test_wetchem.csv")

                try:
                    evaluate.eval(
                        [chemical],
                        f"{os.getcwd()}/outputFiles/{chemical}_test_spc.csv",
                        f"{os.getcwd()}/outputFiles/{chemical}_test_wetchem.csv",
                        f"{os.getcwd()}/outputFiles/predictions",
                        [i for i in models if i in (os.listdir(
                            f"{os.getcwd()}/QC_Model_Predictions/dl_models_all_chems_20210414"))],
                        f"{os.getcwd()}/QC_Model_Predictions/dl_models_all_chems_20210414",
                        "outputFiles/predictions",
                    )
                except Exception as e:
                    print(e)


if __name__ == "__main__":
    call()
