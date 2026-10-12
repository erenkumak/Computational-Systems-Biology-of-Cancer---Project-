# Computational-Systems-Biology-of-Cancer---Project-

## Organization of the github

- **data** folder is used to store input data (main folder) and output data (sub-folder)
- **jupyter notebooks**: the code that should be run, step by step
- other folders are for training

## Description of the steps

### Step 0 - Quality controls

Starting from the raw data of Nestorowa's article, performing quality controls (QC). Used to filter the cells that have low quality or not biologically relevant.

TBD
- Normalize the expression matrix
- Filter out genes based on ??
- Conserve only the most highly variable genes

### Step 1 - Computing clusters with STREAM
STREAM is used to build gene clusters and track the trajectory of cell fates.

### Step 2 - Binarization with PROFILE
From the full scRNA-seq dataset, PROFILE was used to classify in each cell each gene as either 0, 1, or undetermined, by comparing its expression to the distribution in all cells. Genes are are then binarized depending on majority rule, by STREAM cluster group. 

### Step 3 - Generating boolean network with bonesis

