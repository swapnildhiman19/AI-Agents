Creates a new environment for Notebook with ipykernel
Activate that environment
Install jupyterLab so that it (opens the Jupyter Lab Notebook experience on the localhost:8888/lab)
Opens the web experience
Install extension jupyterlab-git, catpuccin-jupyterlab

```sh
conda create -n jupyterLabsEnv python=3.10.0 ipykernel -y
conda activate jupyterLabsEnv 
conda install -c conda-forge jupyterlab
jupyter lab --no-browser --allow-root --ip 0.0.0.0
conda install -c conda-forge jupyterlab-git
conda install -c conda-forge catppuccin-jupyterlab
```