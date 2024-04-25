from pathlib import Path
import os
import shutil


def retrieve_splits():
    path = Path("Z://ML/models_in_production/")
    os.makedirs("./inputFiles/models_in_production", exist_ok=True)
    shutil.copy(path, "./inputFiles/models_in_production")
