#!/bin/bash

##########pre_mol##########

output=$(obabel.exe -i mol2 mol2/pre_mol.mol2 -o smi)

smiles_pre=$(echo "${output}" | awk '{print $1; exit}')
echo "SIMILES ${smiles_pre}"

output=$(echo "${smiles_pre}" | obabel.exe -ismi  -oxyz -h )

atom_smi1=$(echo "${output}" | sed -n '1p')
echo "Atom Number : ${atom_smi1}"

cd pre_EMC
rm pre*
sed  "s/###atomnum/${atom_smi1}/g" init.esh  > ./pre_mol.esh
sed  -i "s/XXXXX/${smiles_pre}/g" pre_mol.esh

emc_setup.pl pre_mol.esh 
emc_win32.exe build.emc > emc.log

cd ../

##########post_mol##########

output=$(obabel.exe -i mol2 mol2/post_mol.mol2 -o smi)

smiles_post=$(echo "${output}" | awk '{print $1; exit}')
echo "SIMILES ${smiles_post}"

output=$(echo "${smiles_post}" | obabel.exe -ismi  -oxyz -h)

atom_smi2=$(echo "${output}" | sed -n '1p')
echo "Atom Number : ${atom_smi2}"

cd post_EMC
rm post*
sed  "s/###atomnum/${atom_smi2}/g" init.esh > ./post_mol.esh
sed  -i "s/XXXXX/${smiles_post}/g" post_mol.esh

emc_setup.pl post_mol.esh
emc_win32.exe build.emc > emc.log

cd ../


##########pack_mol##########
delimiter="."
read -a array <<< "${smiles_pre//$delimiter/ }"
mole1="${array[0]}"
mole2="${array[1]}"

if [ ${#mole1} -gt ${#mole2} ]; then
  temp=$mole1
  mole1=$mole2
  mole2=$temp
fi

echo $mole1
echo $mole2

ratio2=$((100-$2))

cd pack_EMC

rm pack*
sed  "s/XXXXX_1/${mole1}/g" init.esh > ./pack_mol.esh
sed  -i "s/XXXXX_2/${mole2}/g" pack_mol.esh
sed  -i "s/###totalatom/$1/g" pack_mol.esh
sed  -i "s/###ratio1/${ratio2}/g" pack_mol.esh
sed  -i "s/###ratio2/$2/g" pack_mol.esh
emc_setup.pl pack_mol.esh
emc_win32.exe build.emc > emc.log

cd ../


cd automap
rm *.data
cd ../
../concat_param.py

cd automap
AutoMapper.py . molecule pre_mol.data  --save_name pre-mol.data
AutoMapper.py . molecule post_mol.data  --save_name post-mol.data
