##Install Miniconda
https://docs.anaconda.com/miniconda/install/#quick-command-line-install


mkdir -p ~/miniconda3
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh -o ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh


All version URLs can be found here https://repo.anaconda.com/miniconda/

##Setup Miniconda
source ~/miniconda3/bin/activate
conda init --all   
Create a new env
Create a new python env called hello, with python version 3.10.0

conda create --name hello python=3.10.0 -y
Activate the env
conda activate hello
Get Info about current enviroment
We can see things like where the python envs exists.

conda info
Remove an env
conda deactivate
conda remove -n hello --all -y

