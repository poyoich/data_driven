#!/bin/bash

##########pre_mol##########

output=$(obabel.exe -i mol2 mol2/pre_mol.mol2 -o smi)

smiles_pre=$(echo "${output}" | awk '{print $1; exit}')
echo "SIMILES ${smiles_pre}"

output=$(echo "${smiles_pre}" | obabel.exe -i smi -o fh --gen3D)

var=$(echo "${output}" | sed -n '2p')
echo "Atom Number : ${var}"

cd pre_EMC
rm pre*
sed  "s/###atomnum/${var}/g" init.esh  > ./pre_mol.esh
sed  -i "s/XXXXX/${smiles_pre}/g" pre_mol.esh

emc_setup.pl pre_mol.esh 
emc_win32.exe build.emc > emc.log

cd ../

##########post_mol##########

output=$(obabel.exe -i mol2 mol2/post_mol.mol2 -o smi)

smiles_post=$(echo "${output}" | awk '{print $1; exit}')
echo "SIMILES ${smiles_post}"

output=$(echo "${smiles_post}" | obabel.exe -i smi -o fh --gen3D)

var=$(echo "${output}" | sed -n '2p')
echo "Atom Number : ${var}"

cd post_EMC
rm post*
sed  "s/###atomnum/${var}/g" init.esh > ./post_mol.esh
sed  -i "s/XXXXX/${smiles_post}/g" post_mol.esh

emc_setup.pl post_mol.esh
emc_win32.exe build.emc > emc.log

cd ../


##########pack_mol##########
delimiter="."
read -a array <<< "${smiles_pre//$delimiter/ }"
mole1="${array[0]}"
mole2="${array[1]}"

echo $mole1
echo $mole2

cd pack_EMC

rm pack*
sed  "s/XXXXX_1/${mole1}/g" init.esh > ./pack_mol.esh
sed  -i "s/XXXXX_2/${mole2}/g" pack_mol.esh
emc_setup.pl pack_mol.esh
emc_win32.exe build.emc > emc.log

cd ../


../concat_param.py
