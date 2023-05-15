# nbscuid 🦑

### Notebook-Based, Super CUstomizable Infrastructure for Diagnostics

This is a package to enable running notebook-based diagnostic workflows. Based on my-cesm-experiment by matt-long: https://github.com/matt-long/my-cesm-experiment. 

See some examples of workflows at https://github.com/rmshkv/nbscuid-examples.

## Capabilities

- Integration with data catalogs
- Inject custom parameters into code and Markdown cells
- Run many notebooks at once on a parameter set, or different parameters per notebook
- Run different notebooks in different environments
- Cache intermediate data products
- Quickly build a Jupyter book with results


## Installation

1. Clone this repo

2. Activate the environment you want to install `nbscuid` in. Within the cloned `nbscuid` directory, run:
    ```
    pip install .
    ```
    Alternatively, to install the commands `nbscuid-run` and `nbscuid-build` without installing all of `nbscuid`'s dependencies, first install `pipx` with `pip install pipx`, then run:
    ```
    pipx install .
    ```

## Running a notebook collection

Create a new folder that contains a `config.yml` file. (A guide to what goes in a `config.yml` file is coming soon!) This will be the run directory for your collection of notebooks, where all the computed notebooks will appear.

To run all the notebooks you've specified, execute:

```
nbscuid-run path/to/config.yml
```


To build the jupyter book if desired, execute:

```
nbscuid-build path/to/config.yml
```



