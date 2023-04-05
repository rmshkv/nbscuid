import subprocess
import sys
import os

def build():
    
    path_to_dir = os.path.dirname(os.path.abspath(__file__))
    path_to_run = path_to_dir + "/build.py"

    config_path = sys.argv[1]
    subprocess.run(["conda", "run",  "-n", "nbscuid-jupyter-book", "--no-capture-output", "python", path_to_run, config_path])
    
    return None