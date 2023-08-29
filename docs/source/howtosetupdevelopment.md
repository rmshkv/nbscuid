# How to set up an nbscuid development environment

1. Clone the nbscuid repo (on your fork, if desired)

```
git clone https://github.com/rmshkv/nbscuid.git
```

Currently, the active work is being done on the include-ploomber-dev branch. To get on this branch, run:

```
git checkout include-ploomber-dev
```

2. Create and activate an environment

```
conda create -n nbscuid-dev

conda activate nbscuid-dev
```

3. Cd into the top-level nbscuid directory

```
cd nbscuid
```


4. Install nbscuid from source
```
pip install -e .
```

5. Troubleshooting: Check

```
which nbscuid-run
```

# How to set up mom6-tools diagnostics

1. Clone my fork of mom6-tools

```
git clone https://github.com/rmshkv/mom6-tools.git
```

Get onto my dev branch:


```
git checkout nbscuid-compat
```

2. Cd into the directory that contains the diagnostics notebooks (this may move later)
```
cd mom6-tools/mom6-tools/docs/source/examples
```

3. Install the environment that the diagnostics notebooks will run in from the `environment.yml` file:
```
mamba env create -f environment.yml
```
Note that this is different from the nbscuid-dev environment you created earlier, and you *don't* need to activate it.

4. Activate the dev environment you installed nbscuid into previously
```
conda activate nbscuid-dev
```
(or whatever you called your environment)

5. To test out running the notebook collection, make sure you're still in `mom6-tools/mom6-tools/docs/source/examples`, then run:

```
nbscuid-run config.yml
```

6. Make whatever changes you want to the notebooks, config file, and nbscuid code!

