# Scheduler directives
#$ -S /bin/bash
#$ -l h_rt=03:00:00
#$ -l tmem=3G
#$ -l h_vmem=3G
#$ -j y
#$ -cwd
#$ -N GeometricComp
#$ -R y 
#$ -t 1-104

# path to executable of python installed in my environment 
python_poppy="/home/pnikou/.conda/envs/hn_atlas/bin/python3.9"

#root data folder on the cluster
path_to_data="/home/pnikou/Documents/Manc_Data"

#root data folder on the cluster
path_to_excel_file="/home/pnikou/Anonymisation_Key.csv"

patient=$(head -${SGE_TASK_ID} Patients_test.txt | tail -1)
Model=$(head -${SGE_TASK_ID} Models.txt | tail -1)
numcp=$(head -${SGE_TASK_ID} Numcps_test.txt | tail -1)

#path to save log file
path_to_log_file="/home/pnikou/"

# command to run the code 
$python_poppy GeometricComp.py $path_to_data $path_to_excel_file $patient $Model $numcp -u $path_to_log_file