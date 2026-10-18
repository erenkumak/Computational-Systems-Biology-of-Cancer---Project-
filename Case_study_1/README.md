# Case Study 1: Hematopoiesis

## Overview

This repository reproduces **Case Study 1: Hematopoiesis** from Chevalier et al. (2025).

The original code and data are available on [Zenodo](https://doi.org/10.5281/zenodo.16990770). Missing notebooks were implemented based on the methodology described in the associated publications.

## Repository Structure

```text
.
├── Data/
│   └── Input data from Chevalier et al., derived from the Nestorowa et al. hematopoiesis dataset
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
│   └── Conda environment files for STREAM and binarization
└── Results/
    └── Outputs generated at each step of the analysis
```

## Analysis Workflow

The analysis is organized into the following steps:

1. **Data quality control** — assess the quality of the input data.
2. **Data normalization** — normalize the data for downstream analysis.
3. **Trajectory inference** — reconstruct cellular trajectories using STREAM.
4. **Binarization** — convert gene expression data into binary observations.
5. **Component selection** — identify the components used for Boolean network inference.
6. **Component analysis** — characterize the selected components.
7. **Boolean network sampling** — generate Boolean network models using BoNesis.
8. **Ensemble analysis** — analyze the inferred network ensemble, including clustered and interaction-graph analyses.

The corresponding notebooks and scripts are located in the `Code/` directory. Intermediate and final outputs are stored in `Results/`.

## Environment Setup

Conda environment configuration files are provided in the `Environment/` directory.

To create an environment from a YAML file, run:

```bash
conda env create -f Environment/<environment_file>.yml
```

Replace `<environment_file>.yml` with the name of the relevant environment file.

## References

* Chevalier, S., Becker, J., Gui, Y. et al. Data-driven inference of Boolean networks from transcriptomes to predict cellular differentiation and reprogramming. npj Syst Biol Appl 11, 105 (2025). https://doi.org/10.1038/s41540-025-00569-z
* Chen, H. et al. (2019). STREAM: Single-cell Trajectories Reconstruction, Exploration And Mapping of omics data. *Nature Communications*, **10**, 1903.
* Béal, J. et al. (2019). *[An approach for the inference of Boolean networks from gene expression data](https://doi.org/10.3389/fphys.2018.01965)*. *Frontiers in Physiology*, **9**, 1965.
* Nestorowa, S. et al. (2016). A single-cell resolution map of mouse hematopoietic stem and progenitor cell differentiation. *Blood*, **128**, e20–e31.
* Holland, C. H. et al. (2020). DoRothEA: a resource for the inference of transcription factor activities. *Biochimica et Biophysica Acta (BBA) – Gene Regulatory Mechanisms*, **1863**, 194431.
* Chevalier, S., Boyenval, D., Magaña-López, G., Roncalli, T., Vaginay, A. & Paulevé, L. BoNesis: a Python-Based Declarative Environment for the Verification, Reprogramming, and Synthesis of Most Permissive Boolean Networks, pp 71–79. (Springer Nature Switzerland, 2024) https://doi.org/10.1007/978-3-031-71671-3_6.*

## Acknowledgments

This work builds on the datasets, methods, and software developed by the authors cited above.
