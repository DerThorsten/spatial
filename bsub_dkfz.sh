#!/usr/bin/env bash

# using snakemake
#ssh l989o@odcf-lsf01.dkfz.de 'bash -lc "bsub \"cd ~/spatial_deployed; source ~/.bashrc; conda activate spatial-dev; snakemake \""'

# not using snakemake
ssh l989o@odcf-lsf01.dkfz.de 'bash -lc "bsub -q "medium" -M 20000 \"cd ~/spatial_deployed; source ~/.bashrc; conda activate spatial-dev; bash snakemake_not_working.sh \""'
