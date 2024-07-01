import subprocess
import os
from data.getValidAverSpectra import getValidAver, getSpectraforModeling, getSpectralCodes
from data.retrieve_prev_splits import retrieve_splits
from data.getWetchem import getWetchemData
from notebook import run_notebook
import pandas as pd
import shutil
import numpy as np
import gc
from EvaluationTool import evaluate
import multiprocessing

import logging
from pathlib import Path
import datetime

import warnings
warnings.filterwarnings("ignore")

from QC_Model_Predictions.predict import predict_chems
from DSML87.residual_outliers import residual_outliers

today = datetime.datetime.now().strftime("%Y-%m-%d")

modeling_instructions = "/home/tom/DSML125/inputFiles/modeling-instructions.csv"
phone_number = "/home/tom/DSML125/inputFiles/phone_numbers.csv"
evaluation_instructions = "/home/tom/DSML125/inputFiles/model_evaluation.csv"
version = "v2.4"

modelingInstructions = pd.read_csv(modeling_instructions)
chemicals = modelingInstructions['chemical']
instructions = modelingInstructions['instructions']

evaluationInstructions = pd.read_csv(evaluation_instructions)
dataUsed = evaluationInstructions['data_used'].values
modelsUsed = evaluationInstructions['models_used'].values

dataAvailable = [i for i in os.listdir(
        '/home/tom/DSML125/inputFiles/models_in_production')]
modelsAvailable = [i for i in os.listdir(
    '/home/tom/DSML125/QC_Model_Predictions/dl_models_all_chems_20210414')]

chems = [
        # 'aluminium',
        # 'phosphorus',
        'ph',
        # 'exchangeable_acidity',
        'calcium',
        # 'magnesium',
        # 'sulphur',
        # 'sodium',
        # 'iron',
        # 'manganese',
        # 'boron',
        # 'copper',
        # 'zinc',
        # 'total_nitrogen',
        # 'potassium',
        # 'ec_salts',
        # 'organic_carbon', 'cec',
        # 'sand', 'silt', 'clay'
    ]

def checkInitialInputFiles():
    logging.basicConfig(filename='training.log', level=logging.INFO)

    phone_numbers = pd.read_csv(phone_number)
    phone_numbers = phone_numbers['phone']

    

    dataAvailable = [float(str(i).replace("v", "")) for i in os.listdir(
        "/home/tom/DSML125/inputFiles/models_in_production") if "v" in i]
    
    global dataUsed
    dataUsed = [str(i).replace("v", "") for i in dataUsed]
    dataUsed = [str(i).replace(
        "past", "-".join([str(j) for j in dataAvailable if (len(i.split("-")) > 1 and float(j) < float(i.split("-")[1]))])) for i in dataUsed]
    dataUsed = [[f"v{j}" for j in i.split("-")] for i in dataUsed]

    # Ensure that the versions of data and models specified are present. Otherwise make sure to break
    print(dataUsed)
    print([i.split("-") for i in modelsUsed])
    
    print(dataAvailable)
    print(modelsAvailable)

    dataUnavailable = [version for version in [
        i for j in dataUsed for i in j] if version not in dataAvailable]
    modelsUnavailable = [version for version in [i for j in [
        i.split("-") for i in modelsUsed] for i in j] if version not in modelsAvailable]

    print(dataUnavailable)
    print(modelsUnavailable)
    # if (len(dataUnavailable) > 0):
    #     for phone in phone_numbers:
    #         print(phone)
    #         subprocess.run(["python", "sms.py", "--phone", f"{phone}", "--message",
    #                        f"The following data is unavailable {str(','.join(dataUnavailable))}"])
    #     return
    # if (len(modelsUnavailable) > 0):
    #     for phone in phone_numbers:
    #         subprocess.run(["python", "sms.py", "--phone", f"{phone}", "--message",
    #                        f"The following models are unavailable {str(','.join(modelsUnavailable))}"])
    #     return
    # return
    # logging.info(f"Data Used", str(dataUsed))

def removeOldFiles():
    """Preliminary Actions"""
    subprocess.run(['rm', '-rf', '/home/tom/DSML125/outputFiles/spc'])
    subprocess.run(['rm', '-rf', '/home/tom/DSML125/outputFiles/wetchem'])
    subprocess.run(['rm', '-rf', '/home/tom/DSML125/outputFiles/splits'])
    subprocess.run(['rm', '-rf', '/home/tom/DSML125/outputFiles/evaluation'])
    subprocess.run(['rm', '/home/tom/DSML125/outputFiles/spectraldata.csv'])
    subprocess.run(['rm', '-rf', '/home/tom/DSML125/MSSC_DVC/spc'])
    subprocess.run(['rm', '-rf', '/home/tom/DSML125/MSSC_DVC/wetchem'])
    subprocess.run(['rm', '-rf', '/home/tom/DSML125/MSSC_DVC/splits'])
    subprocess.run(['rm', '/home/tom/DSML125/MSSC_DVC/data.zip'])
    subprocess.run(['rm', '-rf', '/home/tom/DSML125/outputFiles/spc'])
    subprocess.run(['rm', '-rf', '/home/tom/DSML125/outputFiles/wetchem'])
    subprocess.run(['rm', '-rf', '/home/tom/DSML125/outputFiles/splits'])
    subprocess.run(['rm', '-rf', '/home/tom/DSML125/outputFiles/predictions'])
    subprocess.run(['rm', '-rf', '/home/tom/DSML125/DSML87/outputFiles/splits'])
    subprocess.run(['rm', '-rf', '/home/tom/DSML125/DSML87/outputFiles/wetchem'])
    subprocess.run(['rm', '-rf', '/home/tom/DSML125/DSML87/outputFiles/spc'])
    subprocess.run(['rm', '-rf', '/home/tom/DSML125/DSML87/outputFiles/PCC_Classes'])
    subprocess.run(['rm', '-rf', '/home/tom/DSML125/DSML87/outputFiles/PCC1'])
    subprocess.run(['rm', '-rf', '/home/tom/DSML125/DSML87/outputFiles/PCC2'])
    subprocess.run(['rm', '-rf', '/home/tom/DSML125/DSML87/outputFiles/PCC3'])
    subprocess.run(['rm', '-rf', '/home/tom/DSML125/DSML87/outputFiles/preds'])
    subprocess.run(['rm', '/home/tom/DSML125/DSML87/outputFiles/cleaned_wetchem.csv'])
    subprocess.run(['rm', '/home/tom/DSML125/DSML87/outputFiles/spectraldata.csv.csv'])
    subprocess.run(['rm', '/home/tom/DSML125/DSML87/outputFiles/wetchem.csv'])
    subprocess.run(['rm', '/home/tom/DSML125/DSML87/outputFiles/md_filtered.csv'])
    subprocess.run(['rm', '/home/tom/DSML125/DSML87/outputFiles/md_outliers.csv'])
    subprocess.run(['rm', '/home/tom/DSML125/DSML87/outputFiles/high_filtered.csv'])
    subprocess.run(['rm', '/home/tom/DSML125/DSML87/outputFiles/high_outliers.csv'])
    subprocess.run(['rm', '/home/tom/DSML125/DSML87/outputFiles/high_filtered.csv'])
    subprocess.run(['rm', '/home/tom/DSML125/DSML87/outputFiles/high_outliers.csv'])
    subprocess.run(['rm', '/home/tom/DSML125/DSML87/outputFiles/hv_filtered.csv'])
    subprocess.run(['rm', '/home/tom/DSML125/DSML87/outputFiles/hv_outliers.csv'])
    subprocess.run(['rm', '/home/tom/DSML125/DSML87/outputFiles/lv_filtered.csv'])
    subprocess.run(['rm', '/home/tom/DSML125/DSML87/outputFiles/lv_outliers.csv'])
    subprocess.run(['rm', '/home/tom/DSML125/DSML87/outputFiles/residual_outliers.csv'])
    subprocess.run(['rm', '/home/tom/DSML125/DSML87/outputFiles/no_residual_outliers.csv'])
    subprocess.run(['rm', '/home/tom/DSML125/DSML87/outputFiles/dl_outliers.csv'])
    subprocess.run(['rm', '/home/tom/DSML125/DSML87/outputFiles/spc_no_residual_outliers.csv'])
    subprocess.run(['rm', '/home/tom/DSML125/DSML87/outputFiles/spc.csv'])

def getValidWetchemAndSpectra():
    getWetchemData(version, chemicals, instructions)
    wet = pd.read_csv(
        '/home/tom/DSML125/inputFiles/uncleaned_wetchem.csv')
    wet = wet.set_index("sample_code")
    wet = wet.sort_values(by=[i for i in chemicals], ascending=True)

    sample_codes = wet.index

    getValidAver(sample_codes)
    os.makedirs("DSML87/inputFiles", exist_ok=True)
    """Copy spc to DSML87"""
    shutil.copy("/home/tom/DSML125/outputFiles/spectraldata.csv",
                "/home/tom/DSML125/DSML87/inputFiles/spectraldata.csv")
    shutil.copy('/home/tom/DSML125/inputFiles/uncleaned_wetchem.csv',
                "/home/tom/DSML125/DSML87/inputFiles/uncleaned_wetchem.csv")

def makePredictions():
    predict_chems('/home/tom/DSML125/QC_Model_Predictions/dl_models_all_chems_20210414/v2.2',
                  '/home/tom/DSML125/DSML87/outputFiles/preds', chems, [version], pd.read_csv('/home/tom/DSML125/outputFiles/spectraldata.csv', index_col=0))

def getResidualOutliers():
    residual_outliers(chems, version)

def highlowValueFilter():
    run_notebook('DSML87', '/home/tom/DSML125/DSML87/high_low_value_filter.ipynb')

def markOutliers():
    run_notebook('DSML87', '/home/tom/DSML125/DSML87/Mark Outliers in Wetchem Data.ipynb')

def getSpectraandWetchemforModeling():
    wetchem = pd.read_csv(
        "/home/tom/DSML125/DSML87/outputFiles/cleaned_wetchem.csv", index_col=0)
    wetchem = wetchem.set_index("sample_code")
    spc = getSpectraforModeling(wetchem.index)
    wetchem = wetchem.loc[(wetchem.index.isin(spc.index))]
    if (len(spc.index) < 1):
        logging.error(f"Not enough spectra for modelling")
    spc.to_csv('/home/tom/DSML125/DSML87/outputFiles/spc.csv')
    wetchem.to_csv('/home/tom/DSML125/DSML87/outputFiles/wetchem.csv')

def train_test_split_data():
    # subprocess.run(['bash', 'r_installation.sh'], check=True)
    os.makedirs("/home/tom/DSML125/DSML87/outputFiles/splits", exist_ok=True)
    os.makedirs("/home/tom/DSML125/DSML87/outputFiles/rds", exist_ok=True)
    subprocess.run(['sudo', 'Rscript', '/home/tom/DSML125/DSML87/splits.r'])

def moveDataToOutputFolder():
    os.makedirs('/home/tom/DSML125/outputFiles/spc', exist_ok=True)
    os.makedirs('/home/tom/DSML125/outputFiles/wetchem', exist_ok=True)
    shutil.copy("/home/tom/DSML125/DSML87/outputFiles/spc.csv", "/home/tom/DSML125/outputFiles/spc/spc.csv")
    shutil.copy("/home/tom/DSML125/DSML87/outputFiles/wetchem.csv",
                "/home/tom/DSML125/outputFiles/wetchem/wetchem.csv")

    os.makedirs(f"/home/tom/DSML125/inputFiles/models_in_production/{version}", exist_ok=True)
    try:
        shutil.copytree("/home/tom/DSML125/DSML87/outputFiles/splits",
                        f"/home/tom/DSML125/inputFiles/models_in_production/{version}/splits")
    except Exception as e:
        logging.info(e)
    try:
        shutil.copytree("/home/tom/DSML125/DSML87/outputFiles/splits", "/home/tom/DSML125/outputFiles/splits")
    except Exception as e:
        logging.info(e)
    """Zip data and push"""
    try:
        shutil.copytree("/home/tom/DSML125/outputFiles/spc", "/home/tom/DSML125/MSSC_DVC/spc")
    except Exception as e:
        logging.info(e)

    try:
        shutil.copytree("/home/tom/DSML125/outputFiles/wetchem", "/home/tom/DSML125/MSSC_DVC/wetchem")
    except Exception as e:
        logging.info(e)

    try:
        shutil.copytree("/home/tom/DSML125/outputFiles/splits", "/home/tom/DSML125/MSSC_DVC/splits")
    except Exception as e:
        logging.info(e)

    try:
        shutil.copytree("/home/tom/DSML125/QC_Model_Predictions/dl_models_all_chems_20210414/v2.2", "/home/tom/DSML125/MSSC_DVC/model")
    except Exception as e:
        logging.info(e)

    logging.info(
        f"These are the spectra {len(pd.read_csv('/home/tom/DSML125/MSSC_DVC/spc/spc.csv', engine='c'))}")
    logging.info(
        f"These are the wetchem {len(pd.read_csv('/home/tom/DSML125/MSSC_DVC/wetchem/wetchem.csv'))}")

def uploadToS3():
    os.chdir(f"/home/tom/DSML125/MSSC_DVC")
    subprocess.run(['zip', '-r', 'data.zip', 'spc',
                   'wetchem', 'splits', 'model'], check=True)

    subprocess.run(['bash', 'dvc_setup.sh'])
    os.chdir("../")

def deployDroplets():
    ips = []
    for chem, instructs in zip(chemicals, instructions):
        print(instructs)
        print(chem)
        if (instructs == 'optimize'):
            branch = 'default-args'
        else:
            branch = 'defaultPaths-Model-Update'
        os.chdir("/home/tom/DSML125/dl")
        subprocess.run(['git', 'checkout', branch])
        subprocess.run(['git', 'pull', 'origin'])

        command = ["bash", f"{os.getcwd()}/dl_spinner.sh", chem]
        ip = subprocess.check_output(command, universal_newlines=True)
        ip = ip.split('\n')[-2]
        ips.append(ip)
    pd.DataFrame({"chemical":chemicals, "ips":ips}).to_csv("/home/tom/DSML125/outputFiles/do_servers.csv")

def retrieveTrainedModels():
    os.chdir("/home/tom/DSML125")
    droplets_df = pd.read_csv("/home/tom/DSML125/outputFiles/do_servers.csv")
    ips = droplets_df['ips'].values
    chemicals = droplets_df['chemical'].values
    for ip, chemical in zip(ips, chemicals):
        subprocess.run(["bash", "remotedatacollector.sh",
                       "--chemical", chemical, "--server", ip, "--version", version])

def evaluateResults():
    os.makedirs("outputFiles/predictions", exist_ok=True)
    for data, models in zip(dataUsed, [str(i).split("-") for i in modelsUsed]):
        # for dataVersion in data:
        for chemical in chemicals:
            print(f"Evaluating for chemical {chemical}")
            # print(dataVersion)
            try:
                test_sample_codes = pd.read_csv(
                    f"{os.getcwd()}/MSSC_DVC/splits/{chemical}_test_sample_codes.csv")
                print(f"Number of test sample codes {len(test_sample_codes)}")
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
                print("Evaluating")
                print(f"Number of wetchem samples: {len(test_wetchem)}")
                print(f"Number of spc samples: {len(test_spc)}")
                evaluate.eval(
                    [chemical],
                    f"{os.getcwd()}/outputFiles/{chemical}_test_spc.csv",
                    f"{os.getcwd()}/outputFiles/{chemical}_test_wetchem.csv",
                    f"{os.getcwd()}/outputFiles/predictions",
                    [i for i in models if i in (os.listdir(
                        f"{os.getcwd()}/QC_Model_Predictions/dl_models_all_chems_20210414"))],
                    f"{os.getcwd()}/QC_Model_Predictions/dl_models_all_chems_20210414",
                    f"outputFiles/predictions/{chemical}/{'-'.join(models)}",
                )
            except Exception as e:
                print(e)




def call(modeling_instructions, phone_number, evaluation_instructions, version):
    gc.enable()
    # subprocess.run(['sudo', 'bash', '/home/tom/DSML125/r_installation.sh'])

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
        "/home/tom/DSML125/inputFiles/models_in_production") if "v" in i]
    dataUsed = [str(i).replace("v", "") for i in dataUsed]
    dataUsed = [str(i).replace(
        "past", "-".join([str(j) for j in dataAvailable if (len(i.split("-")) > 1 and float(j) < float(i.split("-")[1]))])) for i in dataUsed]
    dataUsed = [[f"v{j}" for j in i.split("-")] for i in dataUsed]

    # Ensure that the versions of data and models specified are present. Otherwise make sure to break
    dataAvailable = [i for i in os.listdir(
        '/home/tom/DSML125/inputFiles/models_in_production')]
    modelsAvailable = [i for i in os.listdir(
        '/home/tom/DSML125/QC_Model_Predictions/dl_models_all_chems_20210414')]


    dataUnavailable = [version for version in [
        i for j in dataUsed for i in j] if version not in dataAvailable]
    modelsUnavailable = [version for version in [i for j in [
        i.split("-") for i in modelsUsed] for i in j] if version not in modelsAvailable]

 
    if (len(dataUnavailable) > 0):
        for phone in phone_numbers:
            print(phone)
            subprocess.run(["python", "sms.py", "--phone", f"{phone}", "--message",
                           f"The following data is unavailable {str(','.join(dataUnavailable))}"])
        return
    if (len(modelsUnavailable) > 0):
        for phone in phone_numbers:
            subprocess.run(["python", "sms.py", "--phone", f"{phone}", "--message",
                           f"The following models are unavailable {str(','.join(modelsUnavailable))}"])
        return
    logging.info(f"Data Used", str(dataUsed))

    """Preliminary Actions"""
    os.chdir(f"/home/tom/DSML125/outputFiles")
    subprocess.run(['rm', '-rf', '/home/tom/DSML125/outputFiles'])
    
    os.chdir(f"/home/tom/DSML125/MSSC_DVC")
    subprocess.run(['rm', '-rf', 'spc'])
    subprocess.run(['rm', '-rf', 'wetchem'])
    subprocess.run(['rm', '-rf', 'splits'])
    subprocess.run(['rm', '-rf', f'{version}'])
    os.makedirs(f"/home/tom/DSML125/MSSC_DVC/splits", exist_ok=True)
    os.makedirs(f"/home/tom/DSML125/outputFiles/{version}/splits", exist_ok=True)
    subprocess.run(['rm', 'data.zip'])
    os.chdir(f"/home/tom/DSML125/outputFiles")
    subprocess.run(['rm', '-rf', 'spc'])
    subprocess.run(['rm', '-rf', 'wetchem'])
    subprocess.run(['rm', '-rf', 'splits'])
    subprocess.run(['rm', '-rf', 'predictions'])
    os.chdir(f"/home/tom/DSML125/DSML87")
    subprocess.run(['rm', '-rf', '/home/tom/DSML125/DSML87/outputFiles/splits'])
    subprocess.run(['rm', '-rf', '/home/tom/DSML125/DSML87/outputFiles/wetchem'])
    subprocess.run(['rm', '-rf', '/home/tom/DSML125/DSML87/outputFiles/spc'])
    subprocess.run(['rm', '-rf', '/home/tom/DSML125/DSML87/outputFiles/PCC_Classes'])
    subprocess.run(['rm', '-rf', '/home/tom/DSML125/DSML87/outputFiles/PCC1'])
    subprocess.run(['rm', '-rf', '/home/tom/DSML125/DSML87/outputFiles/PCC2'])
    subprocess.run(['rm', '-rf', '/home/tom/DSML125/DSML87/outputFiles/PCC3'])
    subprocess.run(['rm', '-rf', '/home/tom/DSML125/DSML87/outputFiles/preds'])
    subprocess.run(['rm', '/home/tom/DSML125/DSML87/inputFiles/cleaned_wetchem.csv'])
    subprocess.run(['rm', '/home/tom/DSML125/DSML87/inputFiles/uncleaned_wetchem.csv'])
    subprocess.run(['rm', '/home/tom/DSML125/DSML87/inputFiles/spectraldata.csv'])
    subprocess.run(['rm', '/home/tom/DSML125/DSML87/inputFiles/wetchem.csv'])
    subprocess.run(['rm', '/home/tom/DSML125/DSML87/outputFiles/cleaned_wetchem.csv'])
    subprocess.run(['rm', '/home/tom/DSML125/DSML87/outputFiles/spectraldata.csv'])
    subprocess.run(['rm', '/home/tom/DSML125/DSML87/outputFiles/wetchem.csv'])
    subprocess.run(['rm', '/home/tom/DSML125/DSML87/outputFiles/md_filtered.csv'])
    subprocess.run(['rm', '/home/tom/DSML125/DSML87/outputFiles/md_outliers.csv'])
    subprocess.run(['rm', '/home/tom/DSML125/DSML87/outputFiles/high_filtered.csv'])
    subprocess.run(['rm', '/home/tom/DSML125/DSML87/outputFiles/high_outliers.csv'])
    subprocess.run(['rm', '/home/tom/DSML125/DSML87/outputFiles/high_filtered.csv'])
    subprocess.run(['rm', '/home/tom/DSML125/DSML87/outputFiles/high_outliers.csv'])
    subprocess.run(['rm', '/home/tom/DSML125/DSML87/outputFiles/residual_outliers.csv'])
    subprocess.run(['rm', '/home/tom/DSML125/DSML87/outputFiles/dl_outliers.csv'])
    subprocess.run(['rm', '/home/tom/DSML125/DSML87/outputFiles/spc_no_residual_outliers.csv'])
    subprocess.run(['rm', '/home/tom/DSML125/DSML87/outputFiles/spc.csv'])
    for c in chemicals:
        subprocess.run(['rm', f'outputFiles/{c}_spc.csv'])

    os.chdir(f'/home/tom/DSML125')
    """Get Repos"""
    # subprocess.run(f"{os.getcwd()}/repos.sh")

    """Get subsets"""
    codes = None
    for j in [i for i in Path("/home/tom/DSML125/inputFiles").rglob("**/*subset.csv")]:
        codes = pd.read_csv(j)['sample_code'].values

    """Get available sample codes in new spectral db"""
    availableSpc = getSpectralCodes()

    print("Here are the available spc len ", len(availableSpc))
    
    """Connect to vpn"""
    subprocess.run(["bash", "vpn_con.sh"])

    """Get previous splits"""
    # retrieve_splits()
    """
    Get all averaged spectra
    """

    getWetchemData(version, chemicals, instructions, codes=availableSpc['sample_code'].values)
    wet = pd.read_csv(
        '/home/tom/DSML125/inputFiles/uncleaned_wetchem.csv')
    print("Here are the available wetchem ", len(wet))
    wet = wet.set_index("sample_code")
    wet = wet.sort_values(by=[i for i in chemicals], ascending=True)

    sample_codes = wet.index

    getValidAver(sample_codes)
    

    os.makedirs("DSML87/inputFiles", exist_ok=True)
    """Copy spc to DSML87"""
    shutil.copy("outputFiles/spectraldata.csv",
                "DSML87/inputFiles/spectraldata.csv")
    shutil.copy('/home/tom/DSML125/inputFiles/uncleaned_wetchem.csv',
                "/home/tom/DSML125/DSML87/inputFiles/uncleaned_wetchem.csv")

    """
    Make Predictions
    """
    predict_chems('QC_Model_Predictions/dl_models_all_chems_20210414/v2.2',
                  'DSML87/outputFiles/preds', chems, [version], pd.read_csv('/home/tom/DSML125/outputFiles/spectraldata.csv', index_col=0))

    os.makedirs("/home/tom/DSML125/DSML87/outputFiles/splits", exist_ok=True)
    os.makedirs("/home/tom/DSML125/DSML87/outputFiles/rds", exist_ok=True)
    """Residual Outliers"""
    residual_outliers(chems, version)
    """High Low Value Filter"""
    run_notebook('DSML87', 'high_low_value_filter.ipynb')
    """Mark Outliers"""
    run_notebook('DSML87', 'Mark Outliers in Wetchem Data.ipynb')
    """Get spectra for modelling"""
    gc.collect()
    wetchem = pd.read_csv(
        "/home/tom/DSML125/DSML87/outputFiles/cleaned_wetchem.csv", index_col=0)
    print("Here are the wetchem  ", len(wetchem))
    spc = getSpectraforModeling(wetchem.index)
    print("Here are the spc  ", len(spc))
    spc = spc.drop_duplicates()
    print('HERE IS THE ORIGINAL SPC', len(spc))
    wetchem = wetchem.loc[(wetchem.index.isin(spc.index))]
    if (len(spc.index) < 1):
        logging.error(f"Not enough spectra for modelling")
    
    
    wetchem.to_csv('/home/tom/DSML125/DSML87/outputFiles/wetchem.csv')
    spc.to_csv('/home/tom/DSML125/DSML87/outputFiles/spc.csv')

    """Train Test Split"""
    # subprocess.run(['bash', 'r_installation.sh'], check=True)
    subset_test_samples = {}
    for j in [i for i in Path("/home/tom/DSML125/inputFiles").rglob("**/*subset.csv")]:
        project = j.name
        codes = pd.read_csv(j)['sample_code'].values
        spc_copy = spc.copy(deep=True)
        spc_copy = spc_copy.loc[spc_copy.index.isin(codes)].drop_duplicates()
        for c in chemicals:
            _chem_wet = wetchem[[c]].dropna()
            _chem_spc = spc_copy.loc[spc_copy.index.isin(_chem_wet.index)]
            _chem_spc.to_csv(f'/home/tom/DSML125/DSML87/outputFiles/{c}_spc.csv')
            print(len(_chem_spc))
        print("Splitting subsets")
        [subprocess.run(['sudo', 'Rscript', '/home/tom/DSML125/DSML87/splits.r', f'{c}']) for c in chemicals]
        os.makedirs(f"/home/tom/DSML125/outputFiles/subsets/{project}", exist_ok=True)
        for split in [a for a in Path("/home/tom/DSML125/DSML87/outputFiles/splits").rglob("**/*sample_codes.csv")]:
            if("test_sample_codes" in str(split.name)):
                chem = "_".join(split.name.split("_")[:-3])
                if(chem not in [d for d in subset_test_samples.keys()]):
                    subset_test_samples[chem] = []
                
                subset_test_samples[chem].extend([c for c in pd.read_csv(split, index_col=1).index])
            shutil.copyfile(str(split), f"/home/tom/DSML125/outputFiles/subsets/{project}/{str(split.name)}")
    
    for c in chemicals:
        _chem_wet = wetchem[[c]].dropna()
        _chem_spc = spc.loc[spc.index.isin(_chem_wet.index)]
        print('HERE IS THE chem SPC')
        print(len(_chem_spc))
        _chem_spc.to_csv(f'/home/tom/DSML125/DSML87/outputFiles/{c}_spc.csv')
    print("Splitting main")

    for chemical_name in chemicals:
        subprocess.run(['sudo', 'Rscript', '/home/tom/DSML125/DSML87/splits.r', f'{chemical_name}'])

    shutil.copytree("/home/tom/DSML125/DSML87/outputFiles/splits", f"/home/tom/DSML125/outputFiles")
    shutil.copytree("/home/tom/DSML125/DSML87/outputFiles/splits", f"/home/tom/DSML125/MSSC_DVC")


    """Move Data to output files"""
    os.makedirs('outputFiles/spc', exist_ok=True)
    os.makedirs('outputFiles/wetchem', exist_ok=True)
    shutil.copy("./DSML87/outputFiles/spc.csv", "outputFiles/spc/spc.csv")
    shutil.copy("./DSML87/outputFiles/wetchem.csv",
                "/home/tom/DSML125/outputFiles/wetchem/wetchem.csv")

    os.makedirs(f"inputFiles/models_in_production/{version}", exist_ok=True)
    try:
        shutil.copytree(f"/home/tom/DSML125/outputFiles/{version}/splits",
                        f"/home/tom/DSML125/inputFiles/models_in_production/{version}")
    except Exception as e:
        logging.info(e)
  
    """Zip data and push"""
    try:
        shutil.copytree("/home/tom/DSML125/outputFiles/spc", "/home/tom/DSML125/MSSC_DVC/spc")
    except Exception as e:
        logging.info(e)

    try:
        shutil.copytree("/home/tom/DSML125/outputFiles/wetchem", "/home/tom/DSML125/MSSC_DVC/wetchem")
    except Exception as e:
        logging.info(e)

    try:
        shutil.copytree(f"/home/tom/DSML125/outputFiles/{version}/splits", "/home/tom/DSML125/MSSC_DVC")
    except Exception as e:
        logging.info(e)

    try:
        shutil.copytree("/home/tom/DSML125/QC_Model_Predictions/dl_models_all_chems_20210414/v2.2", "/home/tom/DSML125/MSSC_DVC/model")
    except Exception as e:
        logging.info(e)

    logging.info(
        f"These are the spectra {len(pd.read_csv('/home/tom/DSML125/MSSC_DVC/spc/spc.csv', engine='c'))}")
    logging.info(
        f"These are the wetchem {len(pd.read_csv('/home/tom/DSML125/MSSC_DVC/wetchem/wetchem.csv'))}")


    for j in [i for i in Path("/home/tom/DSML125/inputFiles").rglob("**/*subset.csv")]:
        shutil.copyfile(j,f"/home/tom/DSML125/outputFiles/{today}_subset_{version}.csv")

    for j in [i for i in Path(f"/home/tom/DSML125/outputFiles/{version}").rglob("**/*sample_codes.csv")]:
        shutil.copyfile(j,f"/home/tom/DSML125/MSSC_DVC/{j.name}")
    shutil.copyfile("/home/tom/DSML125/inputFiles/model_evaluation.csv",f"/home/tom/DSML125/outputFiles/{today}_model_evaluation_{version}.csv")
    shutil.copyfile("/home/tom/DSML125/inputFiles/modeling-instructions.csv",f"/home/tom/DSML125/outputFiles/{today}_modeling-instructions_{version}.csv")
    shutil.copyfile("/home/tom/DSML125/inputFiles/uncleaned_wetchem.csv",f"/home/tom/DSML125/outputFiles/{today}_uncleaned_wetchem_{version}.csv")
    # subprocess.run(["rm","-rf",f"/home/tom/DSML125/outputFiles/{version}"])
    # shutil.copytree("/home/tom/DSML125/MSSC_DVC/splits",f"/home/tom/DSML125/outputFiles/{version}")
    shutil.copyfile("/home/tom/DSML125/DSML87/outputFiles/dl_outliers.csv",f"/home/tom/DSML125/outputFiles/{today}_dl_outliers_{version}.csv")
    shutil.copyfile("/home/tom/DSML125/DSML87/outputFiles/dl_outliers.csv",f"/home/tom/DSML125/outputFiles/{today}_hv_outliers_{version}.csv")
    shutil.copyfile("/home/tom/DSML125/DSML87/outputFiles/dl_outliers.csv",f"/home/tom/DSML125/outputFiles/{today}_lv_outliers_{version}.csv")
    shutil.copyfile('/home/tom/DSML125/DSML87/outputFiles/wetchem.csv',f"/home/tom/DSML125/outputFiles/{today}_wetchem_{version}.csv")  
    shutil.copytree('/home/tom/DSML125/DSML87/outputFiles/preds',"/home/tom/DSML125/outputFiles/preds")
    os.makedirs("/home/tom/DSML125/outputFiles/final", exist_ok=True)
    os.makedirs("/home/tom/DSML125/outputFiles/final/done", exist_ok=True)
    return
    # os.chdir(f"{os.getcwd()}/MSSC_DVC")
    # subprocess.run(['zip', '-r', 'data.zip', 'spc',
    #                'wetchem', 'splits', 'model'], check=True)
    

    # subprocess.run(['bash', 'dvc_setup.sh'])
    # os.chdir("../")

    # """Run model optimization update"""

    # ips = []
    # for chem, instructs in zip(chemicals, instructions):
    #     print(instructs)
    #     print(chem)
    #     if (instructs == 'optimize'):
    #         branch = 'default-args'
    #     else:
    #         branch = 'defaultPaths-Model-Update'
    #     os.chdir("/home/tom/DSML125/dl")
    #     subprocess.run(['git', 'checkout', branch])
    #     # subprocess.run(['git', 'pull', 'origin'])

    #     command = ["bash", f"{os.getcwd()}/dl_spinner.sh", chem]
    #     ip = subprocess.check_output(command, universal_newlines=True)
    #     ip = ip.split('\n')[-2]
    #     ips.append(ip)
    # print(ips)
    # os.chdir("/home/tom/DSML125")

    # for ip, chemical in zip(ips, chemicals):
    #     subprocess.run(["bash", "remotedatacollector.sh",
    #                    "--chemical", chemical, "--server", ip, "--version", version])
    # return
    print(dataUsed)
    print(modelsUsed)

    os.makedirs("outputFiles/predictions", exist_ok=True)
    for data, models in zip(dataUsed, [str(i).split("-") for i in modelsUsed]):
        # for dataVersion in data:
        for chemical in chemicals:
            print(f"Evaluating for chemical {chemical}")
            # print(dataVersion)
            try:
                test_sample_codes = pd.read_csv(
                    f"{os.getcwd()}/outputFiles/splits/{chemical}_test_sample_codes.csv")
                print(f"Number of test sample codes {len(test_sample_codes)}")
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
                print("Evaluating")
                print(f"Number of wetchem samples: {len(test_wetchem)}")
                print(f"Number of spc samples: {len(test_spc)}")
                evaluate.eval(
                    [chemical],
                    f"{os.getcwd()}/outputFiles/{chemical}_test_spc.csv",
                    f"{os.getcwd()}/outputFiles/{chemical}_test_wetchem.csv",
                    f"{os.getcwd()}/outputFiles/predictions",
                    [i for i in models if i in (os.listdir(
                        f"{os.getcwd()}/QC_Model_Predictions/dl_models_all_chems_20210414"))],
                    f"{os.getcwd()}/QC_Model_Predictions/dl_models_all_chems_20210414",
                    f"outputFiles/predictions/{chemical}/{'-'.join(models)}",
                )
            except Exception as e:
                print(e)


if __name__ == "__main__":
    call()
