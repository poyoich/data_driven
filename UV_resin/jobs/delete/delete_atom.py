#!/usr/bin/env python3
import numpy as np
import datetime
import sys 

target = int(sys.argv[1])

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
                        self.elem_num = int(spline[0])

                    if spline[1] == "bonds":
                        self.numberOfBonds = int(spline[0])

                    if spline[1] == "bond":
                        self.numberOfBondType = int(spline[0])

                    if spline[1] == "angles":
                        self.numberOfAngs = int(spline[0])

                    if spline[1] == "angle":
                        self.numberOfAngleType = int(spline[0])

                    if spline[1] == "dihedrals":
                        self.numberOfDihedrals = int(spline[0])

                    if spline[1] == "dihedral":
                        self.numberOfDihedralType = int(spline[0])

                    if spline[1] == "impropers":
                        self.numberOfImpropers = int(spline[0])

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

                
                if spline[0] == "Atoms":
                    splines = list( [ l.split() for l in lines[ind+2:ind+2+self.total_particle] ] )
                    
                    for l in splines:
                        self.particles_out.append("\t".join(l))
                        

                if spline[0] == "Bonds":
                    splines = list( [ l.split() for l in lines[ind+2:ind+2+self.numberOfBonds] ] )

                    for l in splines:
                        self.bond_out.append("\t".join(l))

                if spline[0] == "Angles":
                    splines = list( [ l.split() for l in lines[ind+2:ind+2+self.numberOfAngs] ] )

                    for l in splines:
                        self.angle_out.append("\t".join(l))

                if spline[0] == "Dihedrals":
                    splines = list( [ l.split() for l in lines[ind+2:ind+2+self.numberOfDihedrals] ] )
                    for l in splines:
                        self.dihedral_out.append("\t".join(l))

                if spline[0] == "Impropers":
                    splines = list( [ l.split() for l in lines[ind+2:ind+2+self.numberOfImpropers] ] )

                    for l in splines:
                        self.improper_out.append("\t".join(l))
                        
    def export_file(self, ifn, param : parameter):
        header_line = [f"Mody lammps parameter {datetime.datetime.now()}\n"]
        
        header_line.append(f"\t{len(self.particles_out)} atoms")
        header_line.append(f"\t{self.elem_num} atom types")
        header_line.append(f"\t{self.numberOfAngleType} angle types")
        header_line.append(f"\t{self.numberOfBondType} bond types")
        header_line.append(f"\t{self.numberOfDihedralType} dihedral types")
        header_line.append(f"\t{self.numberOfImproperType} improper types\n")
        
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


def is_greater_than(value, threshold):
    if value > threshold:
        return 1
    else:
        return 0

def main():
    param = parameter()
    param.read_param("./calc.pram")

    lmp_data1 = Lammps_data()
    lmp_data1.import_file("./pre_mol.data", param)
    
    ### atoms####
    
    for l in lmp_data1.particles_out:
        sp = l.split()
        if sp[0] == str(target):
            del_charge = float(sp[3])
            break
        #else:
            #sp[0] = str(int(sp[0])-is_greater_than(int(sp[0]),target))
            #particles_out_new.append("\t".join(sp))
    
    
    ### bond###
    bond_out_new = []
    for l in lmp_data1.bond_out:
        sp = l.split()
        if str(target) in sp[2:]:
            del_charge_atom = sp[2] if sp[2] != str(target) else sp[3]
        else:
            for i in range(2,4):
                sp[i] = str(int(sp[i])-is_greater_than(int(sp[i]),target))
            sp[0] = str(len(bond_out_new) + 1)
            bond_out_new.append("\t".join(sp))
            
    ### update charge####
    particles_out_new = []
    for l in lmp_data1.particles_out:
        sp = l.split()
        if sp[0] == str(target):
            pass
        else:
            if sp[0] == str(del_charge_atom):
                sp[3] = str(float(sp[3])-del_charge)
            sp[0] = str(int(sp[0])-is_greater_than(int(sp[0]),target))
            particles_out_new.append("\t".join(sp))
            
    ###ang###
    angle_out_new = []
    for l in lmp_data1.angle_out:
        sp = l.split()
    
        if str(target) in sp[2:]:
            pass
        else:
            for i in range(2,5):
                sp[i] = str(int(sp[i])-is_greater_than(int(sp[i]),target))
            sp[0] = str(len(angle_out_new) + 1)
            angle_out_new.append("\t".join(sp))    

    ###dihed###
    dihedral_out_new = []
    for l in lmp_data1.dihedral_out:
        sp = l.split()
   
        if str(target) in sp[2:]:
            pass
        else:
            for i in range(2,6):
                sp[i] = str(int(sp[i])-is_greater_than(int(sp[i]),target))
            sp[0] = str(len(dihedral_out_new) + 1)
            dihedral_out_new.append("\t".join(sp))
            
    ###improp###
    improper_out_new = []
    for l in lmp_data1.improper_out:
        sp = l.split()

        if str(target) in sp[2:]:
            pass
        else:
            for i in range(2,6):
                sp[i] = str(int(sp[i])-is_greater_than(int(sp[i]),target))
            sp[0] = str(len(improper_out_new) + 1)
            improper_out_new.append("\t".join(sp)) 

    lmp_data1.particles_out = particles_out_new  
    lmp_data1.bond_out = bond_out_new
    lmp_data1.angle_out = angle_out_new
    lmp_data1.dihedral_out = dihedral_out_new
    lmp_data1.improper_out = improper_out_new
    
    lmp_data1.export_file("./deleted.data", param)


#
if __name__ == "__main__":
    main()


