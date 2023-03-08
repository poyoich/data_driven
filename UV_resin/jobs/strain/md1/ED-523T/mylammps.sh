#!/bin/bash

source ~/.bash_profile
mpiexec.hydra -np 24 lmp_mpi -in  in.react > out
