# Computational Systems Biology of Cancer

## Overview

The goal of this project is to reconstruct, reproduce, and extend the computational pipeline developed by Chevalier et al. (2025) for inferring Boolean gene regulatory networks from transcriptomic data and prior biological knowledge.

Starting from the notebooks and code provided by the original authors, we rebuilt the pipeline and implemented missing steps where notebooks or parts of the analysis were not provided. The objective is to create a more complete, reproducible, and readily applicable workflow that can be adapted to different datasets.

We first reproduced Case Study 1: Hematopoiesis, using the original dataset from Nestorowa et al. (2016), to validate our implementation and verify that we could recover the results reported by Chevalier et al. This served as a test case for checking the consistency and reproducibility of the reconstructed pipeline.

Having established this baseline, we then applied the pipeline to a new dataset describing human thymic development and T-cell differentiation from Park et al. (2020). This second case study explores the applicability of the reconstructed workflow to a different biological system and demonstrates its potential for analyzing new datasets.

The overall methodology integrates single-cell RNA sequencing (scRNA-seq), cellular trajectory inference, gene expression binarization, and Boolean network inference to generate ensembles of regulatory networks capable of reproducing observed qualitative cellular behaviors.

## Methodology

The analysis follows four main steps.

### Step 1 — Quality Control

Quality control (QC) is performed on the raw data to identify and filter out low-quality cells and cells that are not biologically relevant to the analysis.

### Step 2 — Cellular Trajectory Inference with STREAM

[STREAM](https://github.com/pinellolab/STREAM) is used to reconstruct cellular differentiation trajectories and identify groups of genes with related expression patterns. This provides a representation of cellular states and potential cell-fate transitions.

### Step 3 — Gene Expression Binarization with PROFILE

[PROFILE](https://doi.org/10.3389/fphys.2018.01965) is used to classify gene expression in individual cells as **0**, **1**, or **undetermined**, based on the distribution of gene expression across cells.

The resulting observations are then aggregated by STREAM-defined cell clusters using a majority-rule approach, producing binarized datasets for Boolean network inference.

### Step 4 — Boolean Network Inference with BoNesis

[BoNesis](https://doi.org/10.1007/978-3-031-71671-3_6) uses constraints derived from the inferred cellular trajectories, together with the binarized observations and prior knowledge of gene regulatory interactions, to generate Boolean network models consistent with the data.

The resulting ensemble of Boolean networks represents alternative regulatory models capable of reproducing the observed qualitative cellular behaviors.

## Repository Organization

This repository contains two applications of the methodology described by Chevalier et al. (2025):

* **Case Study 1 — Hematopoiesis:** analysis based on the hematopoietic differentiation dataset from Nestorowa et al. (2016).
* **Case Study 2 — T-cell differentiation:** analysis of human thymic development and T-cell differentiation, based on Park et al. (2020).

Each case study is organized into its own directory. Refer to the corresponding `README.md` file for details on its data, scripts, computational environments, and results.

## AI Usage Statement

Generative AI tools were used during the development of this project to assist with code generation, debugging, and troubleshooting. All AI-generated suggestions were reviewed and adapted as needed by the authors, who remain responsible for the implementation, analysis, interpretation of results, and conclusions presented in this repository.

## References

1. **Chevalier, S. et al. (2025).** Article in *npj Systems Biology and Applications*, **11**, 105. https://doi.org/10.1038/s41540-025-00569-z

2. **Chen, H. et al. (2019).** STREAM: Single-cell Trajectories Reconstruction, Exploration And Mapping of omics data. *Nature Communications*, **10**, 1903.

3. **Béal, J. et al. (2019).** An approach for the inference of Boolean networks from gene expression data. *Frontiers in Physiology*, **9**, 1965. https://doi.org/10.3389/fphys.2018.01965

4. **Nestorowa, S. et al. (2016).** A single-cell resolution map of mouse hematopoietic stem and progenitor cell differentiation. *Blood*, **128**, e20–e31.

5. **Holland, C. H. et al. (2020).** DoRothEA: a resource for the inference of transcription factor activities. *Biochimica et Biophysica Acta (BBA) – Gene Regulatory Mechanisms*, **1863**, 194431.

6. **Chevalier, S., Becker, J., Gui, Y. et al.** Data-driven inference of Boolean networks from transcriptomes to predict cellular differentiation and reprogramming. npj Syst Biol Appl 11, 105 (2025). https://doi.org/10.1038/s41540-025-00569-z.

7. **Park, J. E. et al. (2020).** A cell atlas of human thymic development defines T cell repertoire formation. *Science*, **367**(6480), eaay3224. https://doi.org/10.1126/science.aay3224

## Acknowledgments

This project builds on datasets, methods, and software developed by the researchers cited above.
