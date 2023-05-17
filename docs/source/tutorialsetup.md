# Tutorial - how to get started with a basic notebook collection

1. Install `nbscuid`. To do this, activate your desired work environment, then run 
        
        pip install nbscuid

2. Clone the `nbscuid-examples` repo: 

        git clone https://github.com/rmshkv/nbscuid-examples.git 
        
    We'll be using the `tutorial` collection.
3. In the directory `nbscuid-examples/tutorial`, install the environment specified by `environment.yml`: 

        conda env create -f environment.yml

    This will create an environment called `nbscuid-tutorial1`.

4. Using your text editor of choice, open the file `nbscuid-examples/tutorial/config.yml`. This file runs the whole notebook collection, and there are many ways to customize it. We'll be editing a few paths to make it work on your machine.
5. In this file, under `data_sources`, edit `run_dir` to be the full path to wherever your copy of `nbscuid-examples/tutorial` is located. Then edit `nb_path_root` to be the path to the `nblibrary` folder within `tutorial`. Usually, below this, you would also want to update `default_kernel_name` to be the environment installed on your machine that you want to run your notebooks in. However, since you just installed the environment `nbscuid-tutorial1`, this is already set correctly.
6. Open a terminal. In this terminal, activate whatever envionment you installed `nbscuid` in.
7. `cd` into the `nbscuid-examples/tutorial` folder.
8. Run 
            
            nbscuid-run config.yml 

    This will run a few simple notebooks showcasing some of `nbscuid`'s capabilities. The executed notebooks get copied to a directory called `computed_notebooks/placeholder-title` created in your `run_dir`.
9. Next, run 

        nbscuid-build config.yml
        
     This will build the Jupyter Book based on the table of contents specified in the `config.yml` file, under Jupyter Book Table of Contents. The html files that make up the Jupyter Book will be created under `computed_notebooks/placeholder-title/_build/html`.

