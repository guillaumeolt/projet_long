#!/usr/bin/env python
# coding: utf-8

# ##projet long prediction of prot prot interactions
# python test to download pdb file, extract prot sequence, set the resolution of the structure

from Bio.PDB import * # set ref
import numpy as np

QIPI = {
'H':1.147, 'R':1.346, 'K':0.784, 'A':0.841, 'V':0.994, 'I':1.084, 'L':1.144, \
'M':1.451, 'P':1.109, 'F':1.334, 'W':1.284, 'Y':1.368, 'G':0.823, 'C':1.172, \
'S':0.873, 'T':0.966, 'N':0.958, 'Q':0.909, 'D':0.830, 'E':0.805}
									
# get pdb file names

def get_structure(name, path, str_structure_id):
    parser = PDBParser()
    return(parser.get_structure(name, path + str_structure_id))

# get the sequence
def get_sequence(structure):
    ppb = CaPPBuilder()
    for pp in ppb.build_peptides(structure):
        polypeptide = pp.get_sequence()
    return(list(polypeptide))
"""
def get_surface_residue(structure, path_structure, rsa_threshold, acc_array = "Sander"):
    list_surface_residue = []
    dssp = DSSP(structure, path_structure, acc_array = acc_array)
    len_chain = []
    sum_len_chain = 0
    for chain in structure:
        len_chain.append(len(chain))
        
    list_dssp = list(dssp)
    print(len(len_chain), "__")
    for i in range(len(len_chain)):
        vec_surface_residue = []
        for j in range(sum_len_chain, sum_len_chain + len_chain[i]):
            print(j, sum_len_chain, len_chain[i])
            if list_dssp[j][3] >= rsa_threshold:
                vec_surface_residue.append([list_dssp[j][0], list_dssp[j][3]])
                
        sum_len_chain =  sum_len_chain + len_chain[i]
        list_surface_residue.append(vec_surface_residue)
        
    return list_surface_residue
"""


def residue_distance(residue_1, residue_2):
    try:
        distance = residue_1['CA'] - residue_2['CA']
    except KeyError:
        print("no CA atoms")
    return distance
"""
def get_interface_residue(structure_1, structure_2, distance_threshold = 8):
    residues_1 = [r for r in structure_1.get_residues()]
    residues_2 = [r for r in structure_2.get_residues()]
    list_interface_residue = []
    vector_interface_1 = np.zeros(len(residues_1))
    vector_interface_2 = np.zeros(len(residues_2))
    print(len(residues_1), len(residues_2))
    for i in range(len(residues_1)):
        for j in range(len(residues_2)):
            distance = residue_distance(residues_1[i], residues_2[j])
            if distance <= distance_threshold:
                list_interface_residue.append([i, j, distance])
                vector_interface_1[i] = 1
                vector_interface_2[j] = 1
    return(list_interface_residue, vector_interface_1, vector_interface_2)
"""

def get_neighbor_residues(structure, residue_middle, k_threshold=9):
    residues = [r for r in structure.get_residues()]
    residue_distance = []
    for i in range(len(residues)):
        distance = residue_middle["CA"] - residues[i]["CA"]#residue_distance(residue_middle, residues[i]) #ERROR with function
        residue_distance.append((i,distance))
    return(sorted(residue_distance, key=itemgetter(1))[0:k_threshold])
    
def get_rsa_relative(path_file_rsa):
    list_relative_rsa = []
    for line in open(path_file_rsa):
        list = line.split()
        id = list[0]
        if id == 'RES':
            relative_rsa = list[5]
            list_relative_rsa.append(float(relative_rsa))
    return(list_relative_rsa)

def get_rsa_relative_bind(path_file_rsa):
    list_relative_rsa = [[]]
    struct_flag = 2
    for line in open(path_file_rsa):
        list = line.split()
        id = list[0]
        
        if id == 'RES':
            res_number = float(list[3])
            if struct_flag == 2:
                struct_flag = 0
            elif struct_flag == 0 and res_number != (res_number_previous+1):
                struct_flag = 1
                list_relative_rsa.append([])
            relative_rsa = list[5]
            list_relative_rsa[struct_flag].append(float(relative_rsa))
            res_number_previous = float(list[3])
    return((list_relative_rsa[0],list_relative_rsa[1]))
    
def get_surface_residue(list_relative_rsa, threshold_rsa = 0.1):
    list_surface_residue = []
    for i in range(len(list_relative_rsa)):
        if list_relative_rsa[i] >= threshold_rsa:
            list_surface_residue.append(i+1)
    return(list_surface_residue)
    
def get_interface_residue(list_relative_rsa, list_relative_rsa_bind):
    list_interface_residue = []
    for i in range(len(list_relative_rsa)):
        if list_relative_rsa[i] != list_relative_rsa_bind[i]:
            list_interface_residue.append(i+1)
    return(list_interface_residue)
            
def count_intersect_surface_interface_residue(list_surface_residue, list_interface_residue):
    k = 0
    for i in range(len(list_surface_residue)):
        for j in range(len(list_interface_residue)):
            if list_surface_residue[i] == list_interface_residue[j]:
                k = k+1
    print(k)
#def get_pssm_value(path_pssm):
    
    
#### MAIN ####
if __name__ == "__main__":
    path_bound = "../data/data_struct3d_bound"
    path_list_bound_pdb_file = path_bound + "/full_structures.0.90.txt"
    
    with open(path_list_bound_pdb_file) as file:
        list_bound_pdb_file = file.readlines()

    print(list_bound_pdb_file[0])

    structure_1 = []
    structure_2 = []
    structure_12 = []
    structure_1.append(get_structure('test_bound_1', path_bound + "/templates/" + list_bound_pdb_file[0][0:-1], '_1.pdb'))
    structure_2.append(get_structure('test_bound_2', path_bound + "/templates/" + list_bound_pdb_file[0][0:-1], '_2.pdb'))
    structure_12.append(get_structure('test_bound_12', path_bound + "/templates_bind/" + list_bound_pdb_file[0][0:-1],'.pdb'))
    ####
    # distance : test, vec1, vec2 = get_interface_residue(structure_1[0], structure_2[0])
    #list_surface_residue = get_surface_residue(structure_1[0][0], path_bound + "/templates/" + list_bound_pdb_file[0][0:-1] + '_1.pdb', 0.1)
    path_file_rsa = path_bound + "/templates/" + list_bound_pdb_file[0][0:-1] + '_1.rsa'
    path_file_rsa_bind = path_bound + "/templates_bind/" + list_bound_pdb_file[0][0:-1] + '.rsa'
    
    list_relative_rsa = get_rsa_relative(path_file_rsa)
    list_relative_rsa_bind = get_rsa_relative_bind(path_file_rsa_bind)
    print(list_relative_rsa)
    print(list_relative_rsa_bind[0])
    list_surface_residue = get_surface_residue(list_relative_rsa)
    list_interface_residue = get_interface_residue(list_relative_rsa, list_relative_rsa_bind[0])
    
    res = [value for value in list_surface_residue if value not in list_surface_residue_12[1]]

    for i in range(len(list_surface_residue)):
        if list_surface_residue[0][0][1] != list_surface_residue_12[0][i][1]:
            print(i)

    list_surface_residue_12[0][0][1]
    list_surface_residue[0][0][1]
    #exemple neighbor
    get_neighbor_residues(structure_1[0], structure_1[0][0]["A"][10], 10)

