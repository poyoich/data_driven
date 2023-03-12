cd pre_EMC
sed -e "s/XXXXX/$1/g" init.esh > pre_mol.esh
emc_setup.pl pre_mol.esh
emc_win32.exe build.emc

cd ../

cd post_EMC
sed -e "s/XXXXX/$2/g" init.esh > post_mol.esh
emc_setup.pl post_mol.esh
emc_win32.exe build.emc

cd ../


python ../concat_param.py