#!/usr/bin/env python3

import itertools
import numpy as np
import datetime

pre_dir = "./pre_EMC/"
post_dir = "./post_EMC/"
pack_dir = "../pack_EMC/"
out_dir = "./automap/"

class parameter:
    def __init__(self):
        self.mass = {}
        self.pair_coeff = {}
        self.bond_coeff = {}
        self.angle_coeff = {}
        self.angle_coeff_bb = {}
        self.angle_coeff_ba = {}
        self.dihedral_coeff = {}
        self.dihedral_coeff_mbt = {}
        self.dihedral_coeff_ebt = {}
        self.dihedral_coeff_at = {}
        self.dihedral_coeff_aat = {}
        self.dihedral_coeff_bb13 = {}
        self.improper_coeff = {}
        self.improper_coeff_aa = {}
        
        self.mass_number = {}
        self.bond_number = {}
        self.angle_number = {}
        self.dihedral_number = {}
        self.improper_number  = {}
    
    def write_param(self,ifn):
        loop_value = {'Masses':self.mass.values(),
                      'Potentials':self.pair_coeff.values(),
                      'Bond Coeffs':self.bond_coeff.values(),
                      'Angle Coeffs':self.angle_coeff.values(),
                      'BondBond Coeffs':self.angle_coeff_bb.values(),
                      'BondAngle Coeffs':self.angle_coeff_ba.values(),
                      'Dihedral Coeffs':self.dihedral_coeff.values(),
                      'MiddleBondTorsion Coeffs':self.dihedral_coeff_mbt.values(),
                      'EndBondTorsion Coeffs':self.dihedral_coeff_ebt.values(),
                      'AngleTorsion Coeffs':self.dihedral_coeff_at.values(),
                      'AngleAngleTorsion Coeffs':self.dihedral_coeff_aat.values(),
                      'BondBond13 Coeffs':self.dihedral_coeff_bb13.values(),
                      'Improper Coeffs':self.improper_coeff.values(),
                      'AngleAngle Coeffs':self.improper_coeff_aa.values()
                      }
        

        with open(ifn,"w") as ofn:
            for key,val in loop_value.items():
                
                ofn.write(f"\n# {key}\n\n")
                ofn.write("".join(list(val)))
            
            

    def read_param(self, ifn):
    
        with open(ifn) as ofn:
            read_lines = ofn.readlines()

        for line in read_lines:
            sp = line.split()
            if len(sp) < 1:
                continue
            if sp[0] == 'mass':
                self.mass[sp[-1]] = line
                
            if sp[0] == "pair_coeff":
                self.pair_coeff[sp[-1]] = line
                
            if sp[0] == "bond_coeff":
                self.bond_coeff[sp[-1]] = line
            
            if sp[0] == "angle_coeff":
                if sp[2] == "bb":
                    self.angle_coeff_bb[sp[-1]] = line
                elif sp[2] == "ba":
                    self.angle_coeff_ba[sp[-1]] = line
                else:
                    self.angle_coeff[sp[-1]] = line
        
            if sp[0] == "dihedral_coeff":
                if sp[2] == "mbt":
                    self.dihedral_coeff_mbt[sp[-1]] = line
                elif sp[2] == "ebt":
                    self.dihedral_coeff_ebt[sp[-1]] = line
                elif sp[2] == "at":
                    self.dihedral_coeff_at[sp[-1]] = line
                elif sp[2] == "aat":
                    self.dihedral_coeff_aat[sp[-1]] = line
                elif sp[2] == "bb13":
                    self.dihedral_coeff_bb13[sp[-1]] = line
                else:
                    self.dihedral_coeff[sp[-1]] = line
                    
            if sp[0] == "improper_coeff":
                if sp[2] == "aa":
                    self.improper_coeff_aa[sp[-1]] = line
                else:
                    self.improper_coeff[sp[-1]] = line
                
def concat_dict(dict1, dict2):
    """
    二つの辞書型を比較してconcatする関数
    """
    # dict1のコピーを作成する
    result_dict = dict1.copy()
    # dict2をresult_dictに追加する
    result_dict.update(dict2)
    return result_dict

def renumber(update_para, name):
    for i,key in enumerate(update_para.keys()):
        sp = update_para[key].split()
        sp[1] = str(i+1)
        if name == "pair_coeff":
            sp[2] = str(i+1)
        update_para[key] = '\t'.join(sp) + "\n"
        
    return update_para

# %%

class Lammps_data:
    def __init__(self):
        
        self.particles_out = []
        self.bond_out = []
        self.angle_out = []
        self.dihedral_out = []
        self.improper_out = []
        self.dcell = [0,0,0]
        self.cell = [0,0,0]
        self.newcell = [0,0,0]
        self.masses = []
        
    def import_file(self, ifn, param : parameter):
        
            with open(ifn, 'r') as ifp:
                lines = ifp.readlines()
            for ind, line in enumerate(lines):
                spline = line.split()
                if len(spline) == 0:
                    continue

                if len(spline) > 1:
                    if spline[1] == "atoms":
                        self.total_particle = int(spline[0])

                    if spline[1] == "atom":
                        elem_num = int(spline[0])

                    if spline[1] == "bonds":
                        numberOfBonds = int(spline[0])

                    if spline[1] == "bond":
                        self.numberOfBondType = int(spline[0])

                    if spline[1] == "angles":
                        numberOfAngs = int(spline[0])

                    if spline[1] == "angle":
                        self.numberOfAngleType = int(spline[0])

                    if spline[1] == "dihedrals":
                        numberOfDihedrals = int(spline[0])

                    if spline[1] == "dihedral":
                        self.numberOfDihedralType = int(spline[0])

                    if spline[1] == "impropers":
                        numberOfImpropers = int(spline[0])

                    if spline[1] == "improper":
                        self.numberOfImproperType = int(spline[0])

                if len(spline) > 3:
    
                    if spline[2] == "xlo":
                        
                        self.dcell[0] = float(spline[0])
                        self.cell[0] = float(spline[1])
                        self.newcell[0] = float(spline[1]) - float(spline[0])

                    if spline[2] == "ylo":
                        self.dcell[1] = float(spline[0])
                        self.cell[1] = float(spline[1])
                        self.newcell[1] = float(spline[1]) - float(spline[0])

                    if spline[2] == "zlo":
                        self.dcell[2] = float(spline[0])
                        self.cell[2] = float(spline[1])
                        self.newcell[2] = float(spline[1]) - float(spline[0])
                
                if spline[0] == "Masses":
                    splines = list([l.split() for l in param.mass.values()])
                    
                    for l in splines:
                        l[-1] = l[-1][0].upper()
                        self.masses.append("\t".join(l[1:]))
                """
                    splines = list( [ l.split() for l in lines[ind+2:ind+2+elem_num] ] )
                    
                    for l in splines:
                        l[-1] = l[-1][0].upper()
                        self.masses.append("\t".join(l))
                """
                
                if spline[0] == "Atoms":
                    splines = list( [ l.split() for l in lines[ind+2:ind+2+self.total_particle] ] )
                    
                    for l in splines:
                        l[2] = param.mass_number[l[-1]]
                        self.particles_out.append("\t".join(l))

                if spline[0] == "Bonds":
                    splines = list( [ l.split() for l in lines[ind+2:ind+2+numberOfBonds] ] )

                    for l in splines:
                        l[1] = param.bond_number[l[-1]]
                        self.bond_out.append("\t".join(l))

                if spline[0] == "Angles":
                    splines = list( [ l.split() for l in lines[ind+2:ind+2+numberOfAngs] ] )

                    for l in splines:
                        l[1] = param.angle_number[l[-1]]
                        self.angle_out.append("\t".join(l))

                if spline[0] == "Dihedrals":
                    splines = list( [ l.split() for l in lines[ind+2:ind+2+numberOfDihedrals] ] )
                    for l in splines:
                        try:
                            l[1] = param.dihedral_number[l[-1]]
                        except:
                            l[1] = param.dihedral_number[",".join(l[-1].split(",")[::-1])]
                        self.dihedral_out.append("\t".join(l))

                if spline[0] == "Impropers":
                    splines = list( [ l.split() for l in lines[ind+2:ind+2+numberOfImpropers] ] )

                    for l in splines:
                        if l[-1] in param.improper_number:
                            tag = l[-1]
                        else:
                            sp = l[-1].split(",")
                            for res in  list(itertools.permutations(sp[1:])):
                                key = sp[0]+","+",".join(list(res))
                                if key in param.improper_number:
                                    tag = key
                                    break
                        l[1] = param.improper_number[tag]
                        self.improper_out.append("\t".join(l))
                        
    def export_file(self, ifn, param : parameter):
        header_line = [f"Mody lammps parameter {datetime.datetime.now()}\n"]
        
        header_line.append(f"\t{self.total_particle} atoms")
        header_line.append(f"\t{len(param.mass_number)} atom types")
        header_line.append(f"\t{len(param.angle_number)} angle types")
        header_line.append(f"\t{len(param.bond_number)} bond types")
        header_line.append(f"\t{len(param.dihedral_number)} dihedral types")
        header_line.append(f"\t{len(param.improper_number)} improper types\n")
        
        header_line.append(f"\t{len(self.bond_out)} bonds")
        header_line.append(f"\t{len(self.angle_out)} angles")
        header_line.append(f"\t{len(self.dihedral_out)} dihedrals")
        header_line.append(f"\t{len(self.improper_out)} impropers\n")
        

        header_line.append(f"\t{self.dcell[0]} {self.cell[0]} xlo xhi")
        header_line.append(f"\t{self.dcell[1]} {self.cell[1]} ylo yhi")
        header_line.append(f"\t{self.dcell[2]} {self.cell[2]} zlo zhi\n\n")
        
        body = ["Masses\n"] + self.masses +["\n"]+ ["Atoms\n"] + self.particles_out + ["\n"] + ["Bonds\n"] + self.bond_out + ["\n"] + ["Angles\n"] \
                           + self.angle_out + ["\n"] + ["Dihedrals\n"] + self.dihedral_out + ["\n"] \
                           + ["Impropers\n"] + self.improper_out + ["\n"]
    
        with open(ifn, "w") as ofn:
            ofn.write("\n".join(header_line))
            ofn.write("\n".join(body))
            

def concat_params(param1, param2):

    concat_param = parameter()
    for var_name in dir(param1):
        if not var_name.startswith("__") and not callable(getattr(param1, var_name)):
            var_value = getattr(param1, var_name)
            #print(f"{var_name}")
            update_para = concat_dict(getattr(param1, var_name),getattr(param2, var_name))
            renumber(update_para, var_name)
            setattr(concat_param, var_name, update_para)
    return concat_param


def main():

    concat_param = parameter()
    concat_param.read_param(pack_dir+"pack_mol.params")

    
    for key, val in concat_param.mass.items():
        index = val.split()[1]
        concat_param.mass_number[key] = index

    for key, val in concat_param.bond_coeff.items():
        index = val.split()[1]
        concat_param.bond_number[key] = index
    
    
    for key, val in concat_param.angle_coeff.items():
        index = val.split()[1]
        concat_param.angle_number[key] = index
        
    
    for key, val in concat_param.dihedral_coeff.items():
        index = val.split()[1]
        concat_param.dihedral_number[key] = index
    
    
    for key, val in concat_param.improper_coeff.items():
        index = val.split()[1]
        sp = key.split(",")
        sp[0],sp[1] = sp[1],sp[0]
        key = ",".join(sp)
        concat_param.improper_number[key] = index
    
    lmp_data1 = Lammps_data()
    lmp_data1.import_file(pre_dir+"pre_mol.data", concat_param)
    lmp_data1.export_file(out_dir+"pre_mol.data", concat_param)
    
    lmp_data2 = Lammps_data()
    lmp_data2.import_file(post_dir+"post_mol.data", concat_param)
    lmp_data2.export_file(out_dir+"post_mol.data", concat_param)
    
    concat_param.write_param(out_dir+"calc.pram")

# %%
if __name__ == "__main__":
    main()


