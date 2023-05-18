import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import os


def run_notebook(repo, file):
    os.chdir(repo)
    filename = file
    with open(filename) as ff:
        nb_in = nbformat.read(ff, nbformat.NO_CONVERT)

    ep = ExecutePreprocessor(timeout=60000000000000, kernel_name='python3')
    nb_out = ep.preprocess(nb_in)
    print("\b")
    os.chdir("../")
