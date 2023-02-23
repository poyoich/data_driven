#!/bin/bash

# 標準出力を変数に格納する


output=$(obabel.exe -i mol2 mol2/pre_mol.mol2 -o smi)

# 1行目の1列目の単語を変数に格納する
smiles=$(echo "${output}" | awk '{print $1; exit}')
echo "SIMILES ${smiles}"

output=$(echo "${smiles}" | obabel.exe -i smi -o fh --gen3D)

# 2行目を変数に格納する
var=$(echo "${output}" | sed -n '2p')
echo "Atom Number : ${var}"

cd pre_EMC
sed  "s/###atomnum/${var}/g" init.esh  > ./pre_mol.esh
sed  -i "s/XXXXX/${smiles}/g" pre_mol.esh

emc_setup.pl pre_mol.esh 
emc_win32.exe build.emc > emc.log

cd ../


output=$(obabel.exe -i mol2 mol2/post_mol.mol2 -o smi)

# 1行目の1列目の単語を変数に格納する
smiles=$(echo "${output}" | awk '{print $1; exit}')
echo "SIMILES ${smiles}"

output=$(echo "${smiles}" | obabel.exe -i smi -o fh --gen3D)

# 2行目を変数に格納する
var=$(echo "${output}" | sed -n '2p')
echo "Atom Number : ${var}"

cd post_EMC
sed  "s/###atomnum/${var}/g" init.esh > ./post_mol.esh
sed  -i "s/XXXXX/${smiles}/g" post_mol.esh

emc_setup.pl post_mol.esh
emc_win32.exe build.emc > emc.log

cd ../

../concat_param.py
