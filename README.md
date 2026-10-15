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
- Feature selection: conserve only the most highly variable genes

### Step 1 - Computing clusters with STREAM
STREAM is used to build gene clusters and track the trajectory of cell fates.

### Step 2 - Binarization with PROFILE
From the full scRNA-seq dataset, PROFILE was used to classify in each cell each gene as either 0, 1, or undetermined, by comparing its expression to the distribution in all cells. Genes are are then binarized depending on majority rule, by STREAM cluster group. 

### Step 3 - Generating boolean network with bonesis

## Applications to a different dataset
Data obtained from the following paper: https://explore.data.humancellatlas.org/projects/c1810dbc-16d2-45c3-b45e-3e675f88d87b
Data file obtained from its repository: https://zenodo.org/records/3572422

We chose to focus on T-cell differenciation trajectory by looking at the human T-cell data, thymus_annotated_matrix_files/HTA08.v01.A06.Science_human_tcells.h5ad. The paper lists expected cell fate trajectories from biological data, which we used to corroborate our STREAM-generated trajectories. 

To find the notebooks for this analysis, explore folder 
