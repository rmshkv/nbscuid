#!/usr/bin/env python

import os
from glob import glob
import papermill as pm
import intake
import nbscuid.util
import nbscuid.cache
import sys
from dask.distributed import Client
import dask
import time

def run():

    # Get control structure
    config_path = str(sys.argv[1])
    control = nbscuid.util.get_control_dict(config_path)
    nbscuid.util.setup_book(config_path)
        
    # Cluster management 
    # Notebooks are configured to connect to this cluster    
    cluster = nbscuid.util.get_Cluster(account=control['account'])
    cluster.scale(4) # Should this be user modifiable?
    
    # Grab paths
    
    ### This code seems repetitive, is there a better way to do this?
    run_dir = control['data_sources']['run_dir']
    output_dir = run_dir + "/computed_notebooks/" + control['data_sources']['casename']
    cache_metadata_path = run_dir + "/cache_metadata_path"
    cache_data_path = run_dir + "/cache_data_path"
    temp_data_path = run_dir + "/temp_data"
    
    nb_path_root = control['data_sources']['nb_path_root']
    
    # Access catalog if it exists

    cat_path = None
    
    if 'path_to_cat_json' in control['data_sources']:
        use_catalog = True
        full_cat_path = control['data_sources']['path_to_cat_json']
        full_cat = intake.open_esm_datastore(full_cat_path)
    
    # Doing initial subsetting on full catalog, e.g. to only use certain cases

        if 'subset' in control['data_sources']:
            first_subset_kwargs = control['data_sources']['subset']
            cat_subset = full_cat.search(**first_subset_kwargs)
            # This pulls out the name of the catalog from the path
            cat_subset_name = full_cat_path.split("/")[-1].split('.')[0] + "_subset"
            cat_subset.serialize(directory=temp_data_path, name=cat_subset_name, catalog_type="file")
            cat_path = temp_data_path + "/" + cat_subset_name + ".json"
        else:
            cat_path = full_cat_path
            
    
    # Grabbing global params if they're included
    
    global_params = dict()
    
    if 'global_params' in control:
        global_params = control['global_params']
        
    
    #####################################################################
    # Organizing notebooks into three lists
    
    precompute_nbs = dict()
    regular_nbs = dict()
    dependent_nbs = dict()

    for nb, info in control['compute_notebooks'].items():
        if 'dependency' in info:
            dependent_nbs[nb] = info

            called_nb = info['dependency']

            precompute_nbs[called_nb] = control['compute_notebooks'][called_nb]
            precompute_nbs[called_nb]["needed by"] = list()
            precompute_nbs[called_nb]["needed by"].append(nb)

        else:
            regular_nbs[nb] = info

    # Removing the precompute nbs that got added to regular_nbs

    for key, item in precompute_nbs.items():
        if key in regular_nbs:
            regular_nbs.pop(key)
            
            
    #####################################################################
    # Pausing to wait for workers to avoid timeout error
           
    dask.config.set({'distributed.comm.timeouts.connect': '90s'})
    
    client = Client(cluster.scheduler_address)
    
    nworkers = 1
    
    waiting_count = 0
    
    while ((client.status == "running") and (len(client.scheduler_info()["workers"]) < nworkers)):
        time.sleep(1.0)
        if waiting_count == 0:
            print("Waiting for Dask workers", end = '')
        else:
            print(".", end = '')
        waiting_count += 1
        
    print("\n")
        
    
    client.close()
    
    
    #####################################################################
    # Calculating precompute notebooks

    ### To do: figure out how to organize the caching code better, keeping the whole block for now
    
    for nb, info in precompute_nbs.items():
    
        parameter_groups = info['parameter_groups']
        use_cluster = info['use_cluster']

        ### passing in subset kwargs if they're provided
        if 'subset' in info:
            subset_kwargs = info['subset']
        else:
            subset_kwargs = {}

        default_params = {}
        if 'default_params' in info:
            default_params = info['default_params']

        for key, parms in parameter_groups.items():


            ### fix this input path (and also organize this code better)
            input_path = f'{nb_path_root}/{nb}.ipynb'
            output_path = (
                f'{output_dir}/{nb}-{key}.ipynb'
                if key != 'none' else f'{output_dir}/{nb}.ipynb'
            )


            result_df = nbscuid.cache.gen_df_query(cache_metadata_path, input_path, 
                                   full_cat_path, first_subset=first_subset_kwargs, 
                                                 second_subset=subset_kwargs,
                                   params=parms)

            if not result_df.empty:
                #if multiple matches exist, grabs an arbitrary one (FIX LATER)
                asset_path = result_df.loc[0,'assets']
                precompute_nbs[nb]["asset_path"] = asset_path
                print("Fetching result from cache")

            else:

                nb_api = pm.inspect_notebook(input_path)

                asset_path = nbscuid.cache.make_filename(cache_data_path, input_path, full_cat_path) + ".nc"

                if nb_api:
                    parms_in = dict(**default_params)
                    parms_in.update(**global_params)
                    parms_in.update(dict(**parms))
                    parms_in['path_to_cat'] = cat_path
                    
                    if use_cluster:
                        parms_in['cluster_scheduler_address'] = cluster.scheduler_address
                    parms_in['subset_kwargs'] = subset_kwargs
                    parms_in['asset_path'] = asset_path
                else:
                    parms_in = {}

                print(f'executing {input_path}')
                o = pm.execute_notebook(
                    input_path=input_path,
                    output_path=output_path,
                    kernel_name=info['kernel_name'],
                    parameters=parms_in,
                    engine_name='md_jinja',
                    jinja_data=parms,
                    cwd=nb_path_root
                )

                nbscuid.cache.make_sidecar_entry(cache_metadata_path, 
                                               input_path, 
                                               full_cat_path, 
                                               asset_path=asset_path, 
                                               first_subset=first_subset_kwargs, 
                                               second_subset= subset_kwargs,
                                               
                                               ### this might need to be changed to parms_in, not parms, to include global parms  
                                               params=parms)

                # this can only properly handle one save per notebook (FIX LATER)
                precompute_nbs[nb]["asset_path"] = asset_path
    
    # Calculating regular notebooks
    
    for nb, info in regular_nbs.items():
    
        nbscuid.util.run_notebook(nb, info, cluster, cat_path, nb_path_root, output_dir, global_params)
    
    # Calculating notebooks with dependencies
    
    for nb, info in dependent_nbs.items():
    
        ### getting necessary asset:
        dependent_asset_path = precompute_nbs[info['dependency']]["asset_path"]
        
        nbscuid.util.run_notebook(nb, info, cluster, cat_path, nb_path_root, output_dir, global_params, dependent_asset_path)

    # Closing cluster
    cluster.close()
    
    return None
    