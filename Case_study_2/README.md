# Case Study 2: T-Cell Differentiation

## Overview

This case study applies the computational pipeline developed by Chevalier et al. (2025) to a new dataset describing human thymic development and T-cell differentiation, based on Park et al. (2020).

The data are available through the [Human Cell Atlas project](https://explore.data.humancellatlas.org/projects/c1810dbc-16d2-45c3-b45e-3e675f88d87b), with the corresponding dataset hosted on [Zenodo](https://zenodo.org/records/3572422).

We focus on the human T-cell dataset, specifically `thymus_annotated_matrix_files/HTA08.v01.A06.Science_human_tcells.h5ad`. The original study describes expected cellular differentiation trajectories based on biological evidence. These trajectories serve as a reference for evaluating and corroborating the trajectories inferred using STREAM.

Some input files for human genome annotation are too large for github access, and can be found here: 
Homo_sapiens.gene_info: https://www.ncbi.nlm.nih.gov/refseq/annotation_euk/Homo_sapiens/108/
msigdb.v2026.1.Hs.symbols.gmt: https://data.broadinstitute.org/gsea-msigdb/msigdb/release/2026.1.Hs/

This case study explores whether the reconstructed pipeline can be applied to a different biological system and used to infer Boolean gene regulatory networks consistent with the observed T-cell differentiation process.

## Repository Structure

```text
Case_Study_2_T_cells/
├── Data/
│   └── Input and processed T-cell dataset
├── Models/
│   └── Boolean network models generated using BoNesis
├── Code/
│   ├── Data_treatment_QC.ipynb
│   ├── Data_treatment_normalization.ipynb
│   ├── STREAM.ipynb
│   ├── Binarization.Rmd
│   ├── Component_selection.ipynb
│   ├── Component_analysis.ipynb
│   ├── Boolean_network_sampling.ipynb
│   ├── Ensemble_analysis.ipynb
│   ├── Ensemble_analysis_clustered.ipynb
│   └── Ensemble_analysis_interactiongraph.ipynb
├── Environment/
│   └── Conda environment files
└── Results/
    └── Outputs generated at each step of the analysis
```

*Note: The tree above describes the intended organization. Adjust filenames and directory contents to match the files actually present in this case study.*

## Analysis Workflow

The analysis consists of the following steps:

1. **Trajectory inference with STREAM** — reconstruct cellular differentiation trajectories and identify groups of cells with related expression profiles.
2. **Gene expression binarization with PROFILE** — classify gene expression into binary states or undetermined values and aggregate observations by STREAM-defined cell clusters.
3. **Component selection** — identify the genes and regulatory components used for Boolean network inference.
4. **Component analysis** — characterize the selected components and assess their relevance to the inferred regulatory system.
5. **Boolean network sampling with BoNesis** — generate Boolean network models consistent with the binarized observations and the specified network constraints.
6. **Ensemble analysis** — analyze the resulting network ensemble, including clustered analyses and interaction graph representations.

The corresponding notebooks and scripts are located in the `Code/` directory. Intermediate and final outputs are stored in `Results/`, while inferred Boolean network models are stored in `Models/`.

## Environment Setup

Conda environment configuration files are provided in the `Environment/` directory.

To create an environment from a YAML file, run:

```bash
conda env create -f Environment/<environment_file>.yml
```

Replace `<environment_file>.yml` with the name of the relevant environment file.

Activate the environment using:

```bash
conda activate <environment_name>
```

Refer to the environment configuration files and the corresponding notebooks for any additional dependencies or execution requirements.

## Analysis of results: comparing trajectories in samples from 7 post-conception weeks (PCW) vs 12 PCW:

# Paper results
In the Park et al paper, the authors found differences in T-cell populations according to the development stage of the organism. 
- At 7 PCW, the lymphoid compartment contained NK cells, γδ T cells, and ILC3s, with very few differentiating αβT cells, with differentiating T cells mostly found at DN stage
- At 12 weeks, the DN cells progressed to SP (single-positive) stage and found an equilibrium in that state
- Past 12 PCW, the paper found an increase in terminally differentiated CD4+ and CD8+ cells

# Our results: 
The T-cell differentiation trajectories for 12PCW and 17PCW were obtained using the STREAM notebook. 


## References

* Chevalier, S. et al. (2025). *Article in npj Systems Biology and Applications*, **11**, 105. https://doi.org/10.1038/s41540-025-00569-z
* Chen, H. et al. (2019). STREAM: Single-cell Trajectories Reconstruction, Exploration And Mapping of omics data. *Nature Communications*, **10**, 1903.
* Béal, J. et al. (2019). [An approach for the inference of Boolean networks from gene expression data](https://doi.org/10.3389/fphys.2018.01965). *Frontiers in Physiology*, **9**, 1965.
* Nestorowa, S. et al. (2016). A single-cell resolution map of mouse hematopoietic stem and progenitor cell differentiation. *Blood*, **128**, e20–e31.
* Holland, C. H. et al. (2020). DoRothEA: a resource for the inference of transcription factor activities. *Biochimica et Biophysica Acta (BBA) – Gene Regulatory Mechanisms*, **1863**, 194431.
* Chevalier, S. et al. (2024). BoNesis: Boolean Network Inference from Constraints. *Publication details to be confirmed.*
* Park, J. E. et al. (2020). A cell atlas of human thymic development defines T cell repertoire formation. *Science*, **367**(6480), eaay3224. https://doi.org/10.1126/science.aay3224

## Acknowledgments

This work builds on the datasets, methodologies, and software developed by the authors cited above.
