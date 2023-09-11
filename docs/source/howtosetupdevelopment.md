# How to set up an nbscuid development environment

1. Clone the nbscuid repo (on your fork, if desired)

```
git clone https://github.com/rmshkv/nbscuid.git
```
Currently, the active work is being done on the include-ploomber-dev branch. To get on this branch, inside the directory you just cloned, run:

```
git checkout include-ploomber-dev
```
2. Cd into the folder with nbscuid source code:

```
cd nbscuid
```

3. Create a development environment:

```
mamba env create -f dev-environment.yml
```
This creates a new environment called `nbscuid-dev` which contains an editable local installation of nbscuid. This means that if you change the nbscuid code in this folder, it will immediately take effect in this environment.

4. Troubleshooting:

Activate your new development environment:

```
conda activate nbscuid-dev
```
Then run:

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

