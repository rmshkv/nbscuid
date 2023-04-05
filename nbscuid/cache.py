import numpy as np
import os as os
import pandas as pd
import xarray as xr
import dask
from dask.distributed import Client
import intake
import glob
import time
import yaml
from collections import ChainMap
import hashlib
import json
import pathlib

# ## unsure which of the imports will actually be necessary, double check later

def get_filename(path):
    """
    Grab just the file name given a path
    """
    name_only = pathlib.PurePosixPath(path).stem
    return name_only

def make_filename(cache_path, diag_path, catalog_path):
    """
    Create the name for the netcdf and sidecar yaml file, if it's determined that a new one needs to be made
    Note there's no extension; either .nc or .yml should be added
    """
    ### include diag_name, catalog_path, and if already exists, some int += 1
    base_filename = cache_path + "/" + get_filename(catalog_path) + "_" + get_filename(diag_path)
    res = glob.glob(base_filename + "*")
    
    if len(res)==0:
        new_filename = base_filename + "_0"
    else:
        int_list = []
        for i in res:
            int_list.append(int(i.split('_')[-1].split('.')[0]))
            ### should have error handling for case where files have wrong format
        max_int = max(int_list)
        new_filename = base_filename + "_" + str(max_int+1)
    
    return new_filename

def make_hash_field(*args):
    """
    Generate a sha256 hash from an arbitrary number of either string or dict arguments
    Note that dictionaries are internally hashed with md5
    """
    
    def dict_hash(dictionary):
        """MD5 hash of a dictionary.
        Taken from https://www.doc.ic.ac.uk/~nuric/coding/how-to-hash-a-dictionary-in-python.html
        """
        dhash = hashlib.md5()
        # We need to sort arguments so {'a': 1, 'b': 2} is
        # the same as {'b': 2, 'a': 1}
        encoded = json.dumps(dictionary, sort_keys=True).encode()
        dhash.update(encoded)
        
        return dhash.hexdigest()
    
    str_to_hash = str()
    
    for i in args:
        if isinstance(i, str):
            str_to_hash += i
        
        elif isinstance(i, dict):
            str_to_hash += dict_hash(i)
            
        else:
            raise TypeError("All columns must be a string or dict")
                        

    h = hashlib.new('sha256')
    h.update(bytes(str_to_hash, 'utf-8'))
    
    return h.hexdigest()


def make_sidecar_entry(cache_path, diag_path, catalog_path, asset_path="No assets", first_subset={}, second_subset={}, params={}, save=True, query=False):
    """
    Create a yaml file with metadata about a diagnostic notebook run. If query is True, the time of execution
    and path to result will not be saved so the yaml can be used to check if the diagnostic has already been
    run. If save is True, the yaml metadata will be saved to a file in the cache.
    """
    
    metadata_dict = dict()
    
    metadata_dict["diagnostic_path"] = diag_path
    metadata_dict["catalog_path"] = catalog_path
    metadata_dict["parameters"] = params
    
    ### check when catalog was last updated
    cat_last_updated = time.asctime(time.localtime(os.path.getmtime(catalog_path)))
    metadata_dict["catalog_last_updated"] = cat_last_updated
    
    ### check when diag was last updated
    diag_last_updated = time.asctime(time.localtime(os.path.getmtime(diag_path)))
    metadata_dict["diagnostic_last_updated"] = diag_last_updated
    
    
    ### combining the two rounds of subsetting
    ### with this function, if any of the keys are the same, the second subset takes priority
    full_subset_dict = dict(ChainMap(second_subset, first_subset))
    metadata_dict["subset"] = full_subset_dict

    
    metadata_dict["hash"] = make_hash_field(metadata_dict["diagnostic_path"],
                                            metadata_dict["catalog_path"],
                                            metadata_dict["parameters"],
                                            metadata_dict["catalog_last_updated"],
                                            metadata_dict["diagnostic_last_updated"],
                                            metadata_dict["subset"])
                                    
        
    ### this is not very flexible, more of a placeholder for now...
    filename = make_filename(cache_path, diag_path, catalog_path)
    

    ### maybe combine the query and save options? is there any case where they wouldn't correspond?
    if not query:
        metadata_dict["assets"] = asset_path
        
        ### get current time (to purge old runs if necessary later?)
        current_datetime = time.asctime(time.localtime())
        metadata_dict["time_executed"] = current_datetime
        
    if save:
        metadata_dict["yml_path"] = filename + ".yml"
        with open(filename + ".yml", 'w') as file:
            sidecar = yaml.dump(metadata_dict, file)
    else:
        sidecar = yaml.dump(metadata_dict)
        
    ### haven't decided yet if this should return the path to the result
    # result_path = None 
    # return result_path

    return metadata_dict

def make_all_yamls_into_df(cache_path):
    """
    Glob all .yml files present in cache_path into a pandas dataframe that can be searched
    """
    
    all_files = glob.glob(cache_path + "/*.yml")

    if len(all_files) == 0:
        return pd.DataFrame()
    
    df_ls=[]

    for filename in all_files:
        with open(filename,'r') as fh:
            # the only way i could figure out to get it to not split the
            # lower dictionary levels into separate columns
            # having them all be in one makes it easier to check if the cache matches
            # and more flexible if some versions of the diag don't have certain kwargs
            df = pd.json_normalize(yaml.safe_load(fh),max_level=0)
        df_ls.append(df)

    new_df = pd.concat(df_ls)
    return new_df

def gen_df_query(cache_path, diag_path, catalog_path, first_subset={}, second_subset={}, params={}):
    """
    Given metadata about a potential diagnostic run, query the cache to see if it has already been run
    """
    
    df_all = make_all_yamls_into_df(cache_path)
    
    ### if cache folder is empty
    if df_all.empty:
        print("Cache is empty!")
        return pd.DataFrame()
    
    query = make_sidecar_entry(cache_path, diag_path, catalog_path, 
                               first_subset=first_subset, second_subset=second_subset, 
                               params=params, save=False, query=True)
    
    query_hash = query["hash"]
    
    df = df_all.where(df_all["hash"] == query_hash)
    df = df.dropna()
        
    if df.empty:
        print("No matching cache entries!")
        return pd.DataFrame()
    elif df.shape[0] > 1:
        # TODO: make this return only the most recently run one, and give a warning
        return df
    else:
        return df

def overall_logic(query_dict):
    """
    Manager function to check cache and run diagnostic
    """
    # very unfinished
    result_path = gen_df_query(**query_dict)
    
    if result_path:
        # access cache
        return result_path
    else:
        # do the requested computation
        result_path = make_sidecar_entry(**query_dict)
        return result_path


def clean_cache(cache_path, startdate=None):
    """
    Check created date of all the yaml files and remove older ones
    """
    if startdate == None:
        files = glob.glob(cache_path + "/*")
        for f in files:
            os.remove(f)
            
    else:
        # do a query, remove both results and sidecar files
        pass
    return None





