# Scheduler directives
#$ -S /bin/bash
#$ -l h_rt=07:00:00
#$ -l tmem=4G
#$ -l h_vmem=4G
#$ -j y
#$ -cwd
#$ -N PSM_LOO
#$ -R y 
#$ -t 1-4

#export lib path
export LD_LIBRARY_PATH=/share/apps/gcc-8.3/lib64:$LD_LIBRARY_PATH

#path to niftireg executables 
export PATH=/SAN/medic/RTIC-MotionModel/software/niftyReg/install/bin:${PATH}
export LD_LIBRARY_PATH=/SAN/medic/RTIC-MotionModel/software/niftyReg/install/bin:${LD_LIBRARY_PATH}

# path to executable of python installed in my environment 
python_poppy="/home/pnikou/.conda/envs/hn_atlas/bin/python3.9"

#root data folder on the cluster
path_to_data="/home/pnikou/Documents/Manc_Data"

#root data folder on the cluster
path_to_excel_file="/home/pnikou/Anonymisation_Key.csv"

#patient=$(head -${SGE_TASK_ID} Model_Patients.txt | tail -1)
numcp=$(head -${SGE_TASK_ID} Numcps_HN19.txt | tail -1)
patient='19'

#path to save log file
path_to_log_file="/home/pnikou/"

# command to run the code 
$python_poppy fitSM_LOO.py $path_to_data $path_to_excel_file $patient $numcp -u $path_to_log_file