import numpy as np
import pandas as pd
import mygene

# Fixer la graine aléatoire
np.random.seed(100)

# ==========================================
# 1.1 & 1.2 : Chargement et vérifications
# ==========================================
counts_path = "../data/nestorowa_singlecell_raw_data_taken_from_original_paper_GSE.txt"

# Lecture du fichier séparé par des tabulations
raw_df = pd.read_csv(counts_path, sep="\t", index_col=0)
raw_counts = raw_df.astype(float)

# Vérifications de sécurité
assert not raw_counts.index.duplicated().any(), "Identifiants de gènes en double détectés !"
assert not raw_counts.isna().any().any(), "Valeurs NA détectées !"
assert (raw_counts.values >= 0).all(), "Counts négatifs détectés !"

print(f"Raw rows: {raw_counts.shape[0]}")
print(f"Raw cells: {raw_counts.shape[1]}")

# ==========================================
# 1.3 : Identification des types de lignes
# ==========================================
ids = raw_counts.index.to_series()

is_endogenous = ids.str.contains(r"^ENSMUSG", regex=True)
is_ercc = ids.str.contains(r"^ERCC[-_]", case=False, regex=True)
is_htseq = ids.str.contains(r"^__", regex=True)
is_unknown = ~(is_endogenous | is_ercc | is_htseq)

summary_df = pd.DataFrame({
    'class': ["ENSMUSG", "ERCC", "HTSeq summary", "unknown"],
    'n': [is_endogenous.sum(), is_ercc.sum(), is_htseq.sum(), is_unknown.sum()]
})
print(summary_df)

if is_unknown.any():
    raise ValueError(f"Lignes inattendues trouvées : {list(ids[is_unknown])}")

# ==========================================
# 1.4 : Gènes mitochondriaux GRCm38
# ==========================================
grcm38_mito_ensembl = [f"ENSMUSG000000{i}" for i in range(64336, 64362)] + \
                      [f"ENSMUSG000000{i}" for i in range(64363, 64373)] + \
                      ["ENSMUSG00000065947"]

assert len(grcm38_mito_ensembl) == 37

is_mito_full = is_endogenous & ids.isin(grcm38_mito_ensembl)
is_nuclear_full = is_endogenous & ~is_mito_full

# ==========================================
# 1.5 : Séparation des matrices
# ==========================================
endogenous_counts = raw_counts.loc[is_endogenous]
ercc_counts = raw_counts.loc[is_ercc]
htseq_counts = raw_counts.loc[is_htseq]

print(f"Endogenous: {endogenous_counts.shape[0]}")
print(f"ERCC: {ercc_counts.shape[0]}")
print(f"HTSeq summary: {htseq_counts.shape[0]}")

# ==========================================
# 1.6 : Seuils de contrôle qualité
# ==========================================
MIN_NUCLEAR_READS = 200000
MIN_DETECTED_GENES = 4000
MAX_MITO_PCT = 10
MAX_ERCC_PCT = 50
NESTOROWA_REPORTED_CELLS = 1656

# ==========================================
# 1.7 : Reconstruction des métriques QC
# ==========================================
def get_htseq_row(row_name):
    if row_name in htseq_counts.index:
        return htseq_counts.loc[row_name].values
    return np.zeros(raw_counts.shape[1])

raw_total_reads = raw_counts.sum(axis=0)
not_aligned = get_htseq_row("__not_aligned")
mapped_reads = raw_total_reads - not_aligned

nuclear_reads = raw_counts.loc[is_nuclear_full].sum(axis=0)
mitochondrial_reads = raw_counts.loc[is_mito_full].sum(axis=0)
ercc_reads = ercc_counts.sum(axis=0)
assigned_feature_reads = endogenous_counts.sum(axis=0) + ercc_reads

# Annotation des gènes codants via MyGeneInfo (équivalent à org.Mm.eg.db)
mg = mygene.MyGeneInfo()
endogenous_ids = ids[is_endogenous].tolist()
res = mg.getgenes(endogenous_ids, fields='type_of_gene', species='mouse')

gene_type_dict = {}
for entry in res:
    gene_id = entry.get('query')
    gene_type_dict[gene_id] = entry.get('type_of_gene', None)

is_protein_coding_list = [gene_type_dict.get(g) == 'protein-coding' for g in endogenous_ids]
is_protein_coding_endogenous = pd.Series(is_protein_coding_list, index=endogenous_counts.index)

print(f"Protein-coding endogenous genes: {is_protein_coding_endogenous.sum()}")

# Détection des gènes exprimés (> 0 counts) par cellule
detected_genes = (endogenous_counts.loc[is_protein_coding_endogenous] > 0).sum(axis=0)

mito_pct_mapped = 100 * mitochondrial_reads / mapped_reads
ercc_pct_mapped = 100 * ercc_reads / mapped_reads

qc = pd.DataFrame({
    'cell': raw_counts.columns,
    'raw_total_reads': raw_total_reads,
    'mapped_reads': mapped_reads,
    'assigned_feature_reads': assigned_feature_reads,
    'nuclear_reads': nuclear_reads,
    'detected_genes': detected_genes,
    'mitochondrial_reads': mitochondrial_reads,
    'ercc_reads': ercc_reads,
    'mito_pct_mapped': mito_pct_mapped,
    'ercc_pct_mapped': ercc_pct_mapped
})

print("\n--- QC Summary ---")
print(qc[["mapped_reads", "nuclear_reads", "detected_genes", "mito_pct_mapped", "ercc_pct_mapped"]].describe())

# ==========================================
# 1.8 : Application des filtres QC
# ==========================================
qc['pass_nuclear'] = qc['nuclear_reads'] >= MIN_NUCLEAR_READS
qc['pass_genes'] = qc['detected_genes'] >= MIN_DETECTED_GENES
qc['pass_mito'] = qc['mito_pct_mapped'] < MAX_MITO_PCT
qc['pass_ercc'] = qc['ercc_pct_mapped'] < MAX_ERCC_PCT

qc['pass_all'] = (
    qc['pass_nuclear'] &
    qc['pass_genes'] &
    qc['pass_mito'] &
    qc['pass_ercc']
)

print(f"\nInput cells: {len(qc)}")
print(f"Post-QC cells: {qc['pass_all'].sum()}")
print(f"Paper: {NESTOROWA_REPORTED_CELLS}")
print(f"Difference: {qc['pass_all'].sum() - NESTOROWA_REPORTED_CELLS}\n")

print(f"Fail nuclear: {(~qc['pass_nuclear']).sum()}")
print(f"Fail genes: {(~qc['pass_genes']).sum()}")
print(f"Fail mito: {(~qc['pass_mito']).sum()}")
print(f"Fail ERCC: {(~qc['pass_ercc']).sum()}")

# ==========================================
# 1.9 : Motifs d'échec
# ==========================================
fail_pattern = (
    np.where(qc['pass_nuclear'], "", "nuclear;") +
    np.where(qc['pass_genes'], "", "genes;") +
    np.where(qc['pass_mito'], "", "mito;") +
    np.where(qc['pass_ercc'], "", "ERCC;")
)
fail_pattern[fail_pattern == ""] = "PASS"
print("\n--- Failure patterns ---")
print(pd.Series(fail_pattern).value_counts())

# ==========================================
# 1.10 : Matrice finale filtrée
# ==========================================
keep_cells = qc.loc[qc['pass_all'], 'cell']

endogenous_qc = endogenous_counts[keep_cells]
ercc_qc = ercc_counts[keep_cells]

# Retrait des gènes non exprimés (somme des counts = 0)
endogenous_qc = endogenous_qc.loc[endogenous_qc.sum(axis=1) > 0]
ercc_qc = ercc_qc.loc[ercc_qc.sum(axis=1) > 0]

assert not endogenous_qc.index.str.contains(r"^__").any()
assert not ercc_qc.index.str.contains(r"^__").any()

print(f"\nFinal retained cells: {endogenous_qc.shape[1]}")
print(f"Endogenous genes: {endogenous_qc.shape[0]}")
print(f"ERCCs: {ercc_qc.shape[0]}")

# ==========================================
# 1.11 : Comparaison avec Chevalier et al.
# ==========================================
try:
    chevalier_raw = pd.read_csv("../data/nestorowa_singlecell_raw_data_taken_from_bonesis_paper.tsv", sep="\t", index_col=0)
    print(f"\nChevalier et al. Cell Count: {chevalier_raw.shape[1]}")
    intersect_cells = set(chevalier_raw.columns).intersection(set(keep_cells))
    print(f"Intersect with this QC: {len(intersect_cells)}")
except FileNotFoundError:
    print("\nFichier Chevalier et al. non trouvé pour la comparaison.")