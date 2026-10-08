"""Module for easily replacing gene names with their reference names (gene information from NCBI)"""

import os
from typing import List, Set, Dict, Tuple


def synonyms_from_NCBI(path_NCBIgeneinfo: str) -> dict:
    """
    Crée un dictionnaire associant chaque nom de gène (et ses synonymes) 
    à son nom de référence NCBI (Symbol).
    """
    gene_synonyms_dict = {}
    reference_names = set()

    with open(path_NCBIgeneinfo, "r", encoding="utf-8", errors="ignore") as file_in:
        for line in file_in:
            # Ignorer les commentaires de l'en-tête NCBI (#tax_id ...)
            if line.startswith("#") or not line.strip():
                continue

            fields = line.strip().split("\t")

            # On vérifie qu'on a bien au moins 11 colonnes (sur les 16 présentes)
            if len(fields) >= 11:
                symbol = fields[2].upper()         # Colonne 3 (index 2) : Symbol de référence
                synonyms_raw = fields[4].upper()   # Colonne 5 (index 4) : Synonyms
                other_symbol = fields[10].upper()  # Colonne 11 (index 10) : Symbol_from_nomenclature

                if symbol == "-" or not symbol:
                    continue

                # Traitement des synonymes séparés par "|"
                synonyms_list = synonyms_raw.split("|") if synonyms_raw != "-" else []
                if other_symbol != "-" and other_symbol:
                    synonyms_list.append(other_symbol)

                # Nettoyage des synonymes inutiles
                cleaned_synonyms = [s for s in synonyms_list if s != "-" and s != symbol]

                # Ajout du symbole officiel
                gene_synonyms_dict[symbol] = symbol
                reference_names.add(symbol)

                # Ajout des alias
                for syn in cleaned_synonyms:
                    if syn not in reference_names and syn not in gene_synonyms_dict:
                        gene_synonyms_dict[syn] = symbol

    return gene_synonyms_dict


def reference_gene_name(gene_name: str, dict_synonyms: dict) -> str:
    """
    Given a gene name, return its reference name.
    
    INPUT
     * dict_synonyms
     * gene_name: the gene name you want its reference name
     
    OUTPUT
     * the synonym considered as the reference name
    """
    
    gene_name = gene_name.upper()
    if gene_name in dict_synonyms:
        return dict_synonyms[gene_name]
    return gene_name


def interaction_list_standardization(interactions_list: List[Tuple[str, str, Dict]], path_NCBIgeneinfo: str):
    """
    Create a copy of the input list of pairwise interactions, with each gene name replaced by its reference name (NCBI symbol).
    
    Require the following functions:
    - synonyms_from_NCBI
    - reference_gene_name
        
    INPUT
     * interactions_list: list of tuples containing string (source) + string (target) + dict (sign = 1 or -1)
     * path_NCBIgeneinfo: path to the NCBI gene information file
     
    OUTPUT
     * list of tuples containing string (source) + string (target) + dict (sign = 1 or -1)
    """
    
    # Get gene data information:
    gene_synonyms_dict = synonyms_from_NCBI(path_NCBIgeneinfo)
    
    # Copy the interactions list by replacing each genename by its reference genename into it:
    standardized_interactions_list = list()
    for interaction in interactions_list:
        source = reference_gene_name(interaction[0], gene_synonyms_dict)
        target = reference_gene_name(interaction[1], gene_synonyms_dict)
        standardized_interactions_list.append((source, target, interaction[2])) 
    
    return standardized_interactions_list


def set_standardization(gene_set: set, synonyms) -> set:
    return {reference_gene_name(gene, synonyms) for gene in gene_set}


def file_standardization(path_input: str, path_NCBIgeneinfo: str, columns_to_standardize: List or Set[str] = [0], sep = "\t"):
    """
    Create a copy of the input file, with each gene name replaced by its reference (NCBI symbol) in the column precised in argument.
    
    Require the following functions:
    - synonyms_from_NCBI
    - reference_gene_name
       
    INPUT
     * path_input: path to the input file in which the names must be standardized.
     * path_NCBIgeneinfo: path to the NCBI gene info file.
     * columns_to_standardize : the columns containing gene names we want to standardize. Columns must start at index 0.
     * sep: the field separator into the input SIF file (the gene data file provided by NCBI is a TSV).
    
    OUTPUT
     * copy of the input file,
     with genes in columns_to_standardize replaced by their reference names (capitalized NCBI symbol).
     The file is named like the input file with, at its end, the extension "_standardized".
    """
    
    # Get gene data information:
    gene_synonyms_dict = synonyms_from_NCBI(path_NCBIgeneinfo)
    
    # Replace gene name with reference gene name into the columns_to_standardize of the input file:
    cols_check = set() #put all elements of columns_to_standardize in a set for complexity 
    for c in columns_to_standardize:
        cols_check.add(c)
    
    with open(path_input, "r") as inputfile:
        to_write = []
        for ligne in inputfile.read().split("\n"):
            if len(ligne) > 1:
                cols = ligne.split(sep)
                ligne_output = ""
                id_col = 0
                for col in cols[:-1]:
                    if id_col in cols_check:
                        ligne_output += reference_gene_name(col, gene_synonyms_dict) + sep
                    else:
                        ligne_output += col + sep
                    id_col += 1
                if id_col in cols_check:
                    ligne_output += reference_gene_name(cols[-1], gene_synonyms_dict)
                else:
                    ligne_output += cols[-1]
                ligne_output += "\n"
                to_write.append(ligne_output)
        
    with open(f"{path_input}_standardized", "x") as outputfile:
        for ligne in to_write:
            outputfile.write(ligne)

            
def observations_standardization(observations_dict: Dict, path_NCBIgeneinfo: str) -> Dict:
    """
    Create a copy of the input dict of observations, with each gene name replaced by its reference name (NCBI symbol).
    
    Require the following functions:
    - synonyms_from_NCBI
    - reference_gene_name
        
    INPUT
     * observations_dict: dict (key = observation identifier, value = dict (key = genename, value = gene status))
     * path_NCBIgeneinfo: path to the NCBI gene information file
    
    OUTPUT
     * dict (key = observation identifier, value = dict (key = reference genename, value = gene status))
    """
    
    # Get gene data information:
    gene_synonyms_dict = synonyms_from_NCBI(path_NCBIgeneinfo)
    
    # Copy the dict of observations by replacing each gene name by its reference name (NCBI symbol) in it:
    standardized_observations_dict = dict()
    
    for k,v in observations_dict.items():
        standardized_observations_dict[k] = dict()
        for component, status in v.items():
            standardized_component = reference_gene_name(component, gene_synonyms_dict)
            standardized_observations_dict[k][standardized_component] = status
    
    return standardized_observations_dict