#!/usr/bin/env python3

import pandas as pd
import os
import subprocess

df = pd.read_excel("./excel.xlsx")


pre1=df['pre_1'][0]
pre2=df['pre_2'][0]
post1=df['post_1'][0]
post2=df['post_2'][0]
post3=df['post_3'][0]
post4=df['post_4'][0]


os.chdir("react1")

os.chdir("pre_EMC")

os.system(f'"s/XXXXX/{pre1}/g" init.esh > pre_mol.esh')
os.system('emc_setup.pl pre_mol.esh')
os.system('emc_win32.exe build.emc')

current_dir = os.getcwd()
os.chdir(os.path.dirname(current_dir))

os.chdir("post_EMC")

os.system(f'"s/XXXXX/{post1}/g" init.esh > post_mol.esh')
os.system('emc_setup.pl post_mol.esh')
os.system('emc_win32.exe build.emc')

current_dir = os.getcwd()
os.chdir(os.path.dirname(current_dir))


os.system('python ../concat_param.py')

current_dir = os.getcwd()
os.chdir(os.path.dirname(current_dir))



os.chdir("react2")

os.chdir("pre_EMC")

os.system(f'"s/XXXXX/{pre1}/g" init.esh > pre_mol.esh')
os.system('emc_setup.pl pre_mol.esh')
os.system('emc_win32.exe build.emc')

current_dir = os.getcwd()
os.chdir(os.path.dirname(current_dir))

os.chdir("post_EMC")

os.system(f'"s/XXXXX/{post2}/g" init.esh > post_mol.esh')
os.system('emc_setup.pl post_mol.esh')
os.system('emc_win32.exe build.emc')

current_dir = os.getcwd()
os.chdir(os.path.dirname(current_dir))


os.system('python ../concat_param.py')

current_dir = os.getcwd()
os.chdir(os.path.dirname(current_dir))
