#!/bin/bash


./delete_atom.py $1 pre_mol.data calc.pram pre_mol_del.data
./delete_atom.py $2 post_mol.data calc.pram post_mol_del.data
