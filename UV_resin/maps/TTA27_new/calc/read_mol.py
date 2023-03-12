with open("pack_mol.data","r") as ofn:
    lines = ofn.readlines()

output = []
for l in lines:
    sp = l.split()
    if len(sp) > 8 and "c3h" in sp:
        sp[2] = "2"
    
    output.append("\t".join(sp))

with open("lmp.data", "w") as ofn:
    ofn.write("\n".join(output))
