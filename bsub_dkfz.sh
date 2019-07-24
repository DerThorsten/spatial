#!/usr/bin/env bash

#ssh l989o@odcf-lsf01.dkfz.de 'bsub bash -lc "source ~/.bashrc; cd ~/spatial_deployed; conda activate spatial-dev; snakemake" '
ssh l989o@odcf-lsf01.dkfz.de 'bash -lc "bsub \"cd ~/spatial_deployed; source ~/.bashrc; conda activate spatial-dev; snakemake \""'