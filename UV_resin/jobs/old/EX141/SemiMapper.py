
import sys
import networkx as nx
import matplotlib.pyplot as plt


def lmp2Graph(ifn):
    with open(ifn, "r") as ofn:
        lines = ofn.readlines()

    G = nx.Graph()

    for ind,l in enumerate(lines):
        sp = l.split()
        if len(sp) < 1:
            continue
        if len(sp) > 1:
    
            if sp[1] == "atoms":
                atomnum = int(sp[0])
            if sp[1] == "bonds":
                bondnum = int(sp[0])
        
        if sp[0] == "Atoms":
        
            atoms_l = lines[ind+2:ind+2+atomnum]
            
            for atom in atoms_l:
        
                atom_sp = atom.split()
                G.add_node(int(atom_sp[0]), label=atom_sp[-1][0].upper())
                #print(int(atom_sp[0]))
                
        if sp[0] == "Bonds":
            bonds_l = lines[ind+2:ind+2+bondnum]
            for bond in bonds_l:
                bond_sp = bond.split()
                G.add_edge(int(bond_sp[2]), int(bond_sp[3]))
    return G

G_pre = lmp2Graph(sys.argv[1])
G_post = lmp2Graph(sys.argv[2])

react_a = 10
react_b = 117

G_pre.add_edge(react_a ,react_b)
G_pre.add_edge(11,112)

G_pre.remove_edge(112,117)
G_pre.remove_edge(10,11)


GM = nx.isomorphism.GraphMatcher(G_pre, G_post)

if GM.is_isomorphic():
    node_mapping = GM.mapping
    with open("semi.map", "w") as ofn:
        ofn.write("this map is created by SemiMapper\n\n")
        ofn.write(f"{G_pre.number_of_nodes()} equivalences\n")
        ofn.write(f"{0} edgeIDs\n\n")
        ofn.write("InitiatorIDs\n\n")
        ofn.write(f"{react_a}\n")
        ofn.write(f"{react_b}\n\n")
        ofn.write("EdgeIDs\n\n")
        ofn.write("Equivalences\n\n")
        ofn.write("\n".join([ "\t".join([str(k), str(v)]) for k,v  in node_mapping.items()]))
        
else:
    print("マッチングできないよ.設定を確かめて")
    
