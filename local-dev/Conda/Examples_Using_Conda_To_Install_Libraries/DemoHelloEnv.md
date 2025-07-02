Create Hello Conda Env
Activate environment
Install specific libraries using Conda-forge
We observed which packages are installed under (hello) environment and which packages are installed under (base) environment 
Check what binary is being loaded
 

```sh
conda create -n hello python=3.10.0 -y
conda activate hello
conda install -c conda-forge pandas
pip list 
conda deactivate 
pip list 
conda activate hello
python DemoPandasApp.py
whereis python 
whereis python3
pip install requirements.txt
```