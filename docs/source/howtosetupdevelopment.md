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

# How to do this for the mom6-tools examples

1. Clone my fork of mom6-tools

```
git clone https://github.com/rmshkv/mom6-tools.git
```

Get onto my dev branch:


```
git checkout nbscuid-compat
```

2. The nbscuid-relevant stuff lives in `mom6-tools/docs/source/examples` (for now)

3. Figure out which of your environments can run all the notebooks, and change this in the config.yml file under
```
    default_kernel_name: mom6_solutions
```
(my environment is called mom6_solutions). Most notably this environment should contain mom6-tools.

4. Activate the dev environment you installed nbscuid into previously
```
conda activate nbscuid-dev
```
(or whatever you called your environment)

5. To test out running the notebook collection, make sure you're in the examples folder, then run:

```
nbscuid-run config.yml
```

6. Make whatever changes you want to the notebooks, config file, and nbscuid code!

