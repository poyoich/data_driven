import sys
from rdkit import Chem

# mol2ファイルを読み込み、Moleculeオブジェクトを作成する
mol = Chem.MolFromMol2File(sys.argv[1])
mol = Chem.RemoveHs(mol)

# MoleculeオブジェクトをSMILES表記に変換する
smiles = Chem.MolToSmiles(mol)

# SMILES表記を出力する
print(smiles)
