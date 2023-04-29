from pathlib import Path
import os
import shutil


def retrieve_splits():
    path = Path("Z://ML/models in production/")
    os.makedirs("./inputFiles/models in production", exist_ok=True)
    shutil.copy(path, "./inputFiles/models in production")


retrieve_splits()
