echo [$(date)]: "START"
echo [$(date)]: "creating environment"
conda create --prefix ./env python=3.7 -y

echo [$(date)]: "activate environment"
source activate ./env                 # Or use conda instead of source

echo [$(date)]: "install requirements"
pip install -r requirements.txt

echo [$(date)]: "export conda environment"
conda env export > conda.yaml

echo [$(date)]: "initialize git repository"
git init

echo [$(date)]: "add env to gitignore"
echo "env/" > .gitignore

echo "# ${PWD}" > README.md

echo [$(date)]: "first commit"
git add .

git commit -m "first commit"
echo [$(date)]: "END"

to remove everything -
rm -rf env/ .gitignore conda.yaml README.md .git/