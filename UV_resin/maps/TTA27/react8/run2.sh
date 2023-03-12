cd pre_EMC
rm pre_mol.data
emc_setup.pl pre_mol.esh
emc_win32.exe build.emc

cd ../

cd post_EMC
rm post_mol.data
emc_setup.pl post_mol.esh
emc_win32.exe build.emc

cd ../


rm automap/post_mol.data
rm automap/pre_mol.data
python ../concat_param.py

cd automap
AutoMapper.py . molecule post_mol.data  --save_name post-mol.data
AutoMapper.py . molecule pre_mol.data  --save_name pre-mol.data
