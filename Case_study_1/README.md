# Case Study 1: hematopoiesis

This case study is a reproduction of the case study 1 of the Chevalier et al paper "Data-driven inference of Boolean networks from transcriptomes to predict cellular differentiation and reprogramming". Our goal was to reproduce the paper results and build a comprehensive github interface from which the full analysis pipeline can be conducted on any new dataset. We therefore used the existing jupyter notebooks from the zenodo repository from the paper (https://doi.org/10.5281/zenodo.16990770) where we could, and built the missing jupyter notebooks using the methodology papers cited or by following the method as closely as possible. 

## Organization of the case 1 folder
-  **Data**: used to store input data extracted directly from the Chevalier et al paper, which sources from Nestorowa et al dataset on hematopoiesis.
  - **Models**: stores models built from BoNesis   
- **Code** : Stores jupyter notebooks for each step in the case 1 pipeline and their order.
  - Data_treatment_QC.ipynb
  - Data_treatment_normalization.ipynb
  - STREAM.ipynb
  - Binarization.Rmd
  - Component_selection.ipynb
  - Component_analysis.ipynb
  - Boolean_network_sampling.ipynb
  - Ensemble_analysis.ipynb
  - Ensemble_analysis_clustered.ipynb
  - Ensemble_analysis_interactiongraph.ipynb
- **Environment**: yml files for building corresct conda environments with adapted dependencies for STREAM and binarization
- **Results**: outputs for each script (listed in their respective folder per jupyter notebook)

## References for data abnd methods: 

Main paper: Chevalier, S., Becker, J., Gui, Y. et al. Data-driven inference of Boolean networks from transcriptomes to predict cellular differentiation and reprogramming. npj Syst Biol Appl 11, 105 (2025). https://doi.org/10.1038/s41540-025-00569-z

STREAM (building trajectories): Chen, H. et al. Single-cell trajectories reconstruction, exploration and mapping of omics data with stream. Nat. Commun. 10, 1903 (2019)

PROFILE (binarizing scRNA-seq data): Béal, J., Montagud, A., Traynard, P., Barillot, E. & Calzone, L. Personalization of logical models with multi-omics data allows clinical stratification of patients. Front. Physiol. 9, 1965 (2019).

Nestorowa dataset used in case 1: Nestorowa, S. et al. A single-cell resolution map of mouse hematopoietic stem and progenitor cell differentiation. Blood 128, e20–e31 (2016).

DoRothEA database (for building gene networks): Holland, C. H., Szalai, B. & Saez-Rodriguez, J. Transfer of regulatory knowledge from human to mouse for functional genomics analysis. Biochim. Biophys. Acta 1863, 194431 (2020). Transcriptional Profiles and Regulatory Gene Networks.

BoNesis: Chevalier, S., Boyenval, D., Magaña-López, G., Roncalli, T., Vaginay, A. & Paulevé, L. BoNesis: a Python-Based Declarative Environment for the Verification, Reprogramming, and Synthesis of Most Permissive Boolean Networks, pp 71–79. (Springer Nature Switzerland, 2024) https://doi.org/10.1007/978-3-031-71671-3_6.
