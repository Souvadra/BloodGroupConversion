#!/usr/bin/env python

try: 
    from Bio.PDB.PDBParser import PDBParser
    from Bio.PDB.Polypeptide import three_to_one
except ImportError:
    import sys
    sys.stderr.write("\nERROR: This script requires that Biopython (http://biopython.org) is installed.\n\n")
    sys.exit()

import sys
import os 

def usage():
    print("Pulls gasta file of a specific chain up to a specified output file")
    print("python pdb2fasta.py <directory/of/pdb-s/> <chain> <output>")

if (len(sys.argv) < 3):
   usage()
   exit()

parser = PDBParser(PERMISSIVE=1)

#if sys.argv[3]:
#    stop = int(sys.argv[3])
#else:
stop = ""

open(sys.argv[3], 'a').write("")

# global set variable for all the three letter amino acids 
AA = {"ALA", "ARG", "ASP", "ASN", "CYS", "GLU", "GLN", "GLY", "HIS", "ILE", "LEU", "LYS","MET","PHE","PRO","SER","THR","TRP","TYR","VAL"}

def get_three_letter(pdb, chain_id):
    fasta_three = []
    for model in pdb.get_list():
       for chain in model.get_list():
            if chain.get_id() == chain_id:
               for resi in chain.get_list():
                   fasta_three.append(resi.get_resname())
    return fasta_three

def get_one_letter(list_of_three):
    fasta_one=[]
    for x in list_of_three:
        if x == "S56" or x == "TES":
            x="N"
            fasta_one.append(x)
        else:
            if x in AA:
                x=three_to_one(x)
                fasta_one.append(x)
            else:
                #print(x)
                pass
    return fasta_one


def output_to_file(one_letter, file):
    file_handle = open(sys.argv[3], 'a')
    file_handle.write(">" + file.split('.')[0] + "\n")
    file_handle.write("".join(one_letter) + "\n")
    file_handle.close()


#for file in open(sys.argv[1]).readlines():
path = sys.argv[1]
file_names = os.listdir(path)
for file in file_names:
    file = path + file
    handle = open(file)
    struct = parser.get_structure("random",handle)
    three_letter = get_three_letter(struct, sys.argv[2])
    one_letter = get_one_letter(three_letter)
    output_to_file(one_letter,sys.argv[1])

