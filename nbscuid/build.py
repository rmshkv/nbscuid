#!/usr/bin/env python

import subprocess
import sys
import os
import yaml

if __name__ == '__main__':

    # is it possible to carry this over from the previous call to run.py?
    config_path = str(sys.argv[1])
    
    with open(config_path, "r") as fid:
        control = yaml.safe_load(fid)
    
    casename = control["data_sources"]["casename"]
    run_dir = control["data_sources"]["run_dir"]

    subprocess.run(["jupyter-book", "clean" , f"{run_dir}/computed_notebooks/{casename}"])
    subprocess.run(["jupyter-book",  "build" , f"{run_dir}/computed_notebooks/{casename}",  "--all"])
                   
    if 'publish_location' in control:
        
        user = os.environ.get('USER')
        remote_mach = control["publish_location"]["remote_mach"]
        remote_dir = control["publish_location"]["remote_dir"]
# this seems more complicated than expected...people have mentioned paramiko library?
        # subprocess.run(["mkdir", "-p", remote_dir])
        # subprocess.run(["scp", "-r", f"{run_dir}/computed_notebooks/{casename}/_build/html/*", f"{user}@{remote_mach}:{remote_dir}"])

