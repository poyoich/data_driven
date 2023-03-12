cd pre_EMC
emc_setup.pl pre_mol.esh
emc_win32.exe build.emc

cd ../

cd post_EMC
emc_setup.pl post_mol.esh
emc_win32.exe build.emc

cd ../


python ../concat_param.py
