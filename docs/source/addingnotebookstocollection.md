# How to add diagnostics notebooks

1. Put your new diagnostic notebook in the folder called `nblibrary`.
2. In your notebook, move all variables you might want to change (paths to data, dates to select, etc.) to a cell near the top. For example:

	    sname = "run_name"
	    data_path = "path/to/data"
	    dates = {"start_date" = "01/01/01",
	    			    "end_date" = "01/01/02"}

	To make this super easily compatible with existing `mom6-tools` diagnostics, I've stuck all the global parameters accessed by all the notebooks under a dictionary called `diag_config_yml`, but this is totally optional as long as your notebook is accessing the parameter by its variable name.

3. Right below this cell, paste in two cells that make the notebook compatible with `nbscuid`. Open up `nblibrary/testnb.ipynb` and select the cells below the title:



		# Empty cell with "parameters" tag, papermill-provided parameters will be inserted below.
	### Connecting to cluster
		from dask.distributed import Client
		if cluster_scheduler_address is None:
		    pass
		else:
            client = Client(cluster_scheduler_address)

            client
	With these cells selected (shift-click to select multiple), right click and select "copy cells". Then, in your notebook, right click on your parameters cell, and select "paste cells below."

	*Note: You need to paste notebook cells rather than just the code above, because the cell that looks like it just has the parameters comment actually has a special tag attached that allows papermill to see it. See [papermill's documentation](https://papermill.readthedocs.io/en/latest/usage-parameterize.html) to see how to do this yourself!*

4. Open `config.yml`. First, add your new notebook (as its name, minus the `.ipynb`) to the list of notebooks that will be computed (`compute_notebooks`). For example:

		your_new_nb_name:
		    use_cluster: True  # True if you want the global Dask cluster passed in, otherwise False
			    parameter_groups:
				    none:
						param_specific_to_this_nb: some_value
						another_param: another_value
	If you just want the notebook run once on one set of parameters, keep the`parameter_groups: none:` notation as above. If you want the notebook executed multiple times with different parameter sets, see [this config.yml](https://github.com/rmshkv/nbscuid-examples/blob/main/tutorial/config.yml) for an example of setting this up.

5. If you'd like your new notebook included in the final Jupyter Book, add it to the Jupyter Book table of contents (`book_toc`). See [Jupyter Book's documentation](https://jupyterbook.org/en/stable/structure/toc.html) for different things you can do with this.
6. Update your parameters. Parameters that are specific to just this notebook should go under `parameter_groups` in the notebook's entry under `compute_notebooks`. Global parameters that you want passed in to every notebook in the collection should go under `global_params`.  When `nbscuid` executes your notebook, all of these parameters will get put in a new cell below the special empty cell tagged `"parameters"` that you pasted in earlier. This means they will supercede the values of the parameters that you put in the cell above---the names, notation, etc. should match to make sure your notebook is able to find the variables it needs.
7. All set! Your collection can now be run and built with `nbscuid-run config.yml` and `nbscuid-build config.yml` as usual.
