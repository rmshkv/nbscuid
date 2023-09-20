# Tutorial 1 - how to get started with a basic notebook collection

1. Clone the `nbscuid-examples` repo: 

        git clone https://github.com/rmshkv/nbscuid-examples.git 
        
    We'll be using the `tutorial` collection.
    
2. `cd` into the directory `nbscuid-examples/tutorial`, install the environment specified by `environment.yml`: 

        conda env create -f environment.yml

    This will create an environment called `nbscuid-tutorial1`, which has `nbscuid` installed, as well as the packages necessary to run the tutorial notebooks.

3. Activate the environment you just installed:
        
        conda activate nbscuid-tutorial1

4. Run 
            
        nbscuid-run config.yml 

    This will run a few simple notebooks showcasing some of `nbscuid`'s capabilities. The executed notebooks get copied to a directory called `computed_notebooks/placeholder-title` created in the `run_dir` specified in your `config.yml` (by default the same directory that `config.yml` is in).

5. Next, run 

        nbscuid-build config.yml
        
     This will build the Jupyter Book based on the table of contents specified in the `config.yml` file, under Jupyter Book Table of Contents. The html files that make up the Jupyter Book will be created under `computed_notebooks/placeholder-title/_build/html`.

