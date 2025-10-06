Initialise the virtual environment
Unix system:
python3 -m venv env
Windows:
python -m venv env

Activate the virtual environment:
source env/bin/activate

Install the dependencies:
pip install -r requirements.txt

To execute the code please refer to the final/ folder then navigate to code/. Inside here there is the algorithm/ folder where all the code 
implementations of all the algorithms situate, and then the main/ folder for the main.py where everything is put together and executed. Inside the
config.py, there is all the setting for the running the code just uncomment for the desire algorithm it will product a .zip file for the IOH inside the
folder of doc/data/. After tweaking the config.py, use the command:
    python3 main.py or python main.py

Where to find the submission files
All the code for the algoritms: final/code/algorithms
Proofs: final/doc/analysis/proof
Plots, analysis: final/doc/analysis/Assignment_2_Analysis.pdf
Backup zips for IOH: final/data/
Team contribution: final/doc/team_contribution.txt