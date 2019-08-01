=================================================
Integrative analysis of single cell imaging mass citometry data of breast cancer patients
=================================================

.. image:: https://readthedocs.org/projects/spatial/badge/?version=latest
        :target: http://spatial.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status               

      
.. image:: https://circleci.com/gh/DerThorsten/spatial/tree/master.svg?style=svg
        :target: https://circleci.com/gh/DerThorsten/spatial/tree/master
        :alt: CircleCI Status
      

Current features include: 
  * modern C++ 14
  * build system with modernish CMake 
  
Running a first exploratory data analysis
================
First, install the dependencies with

``conda env create -f spatial-dev-requirements.yml``

and activate the corresponding conda environment

``conda activate spatial-dev``


Currently, there is a problem in the DFKZ cluster which prevents Snakemake to be installed automatically from the ``.yml`` file, so in any machine you also need to run (from within the spatial-dev environment) the following:

``conda install -c bioconda snakemake``


=======
If this still does not work, you need to run the script manually instead that with Snakemake.
Now, if you are in DKFZ cluster the data is already present (in ``/icgc/dkfzlsdf/analysis/B260/projects/spatial_zurich/data``) so, if you have been able to install Snakemake, you can run the exploratory data analysis simply with the command
=======
Now, if you are in DKFZ cluster the data is already present (in ``/icgc/dkfzlsdf/analysis/B260/projects/spatial_zurich/data``) so you can run the exploratory data analysis simply with the command
>>>>>>> c269ac8d28bf8a4b3417ffcbabd34b50ff875ea6



=======
``snakemake``

If you are not in the cluster you first need to update the code in ``folders.py`` by inserting the path of the root folder of the data in your machine. In the root folder the data must be organized into this directory tree:

::

    <data_root_folder>/
    ├── csv/
    │   ├── Basel_PatientMetadata.csv
    │   ├── Basel_Zuri_SingleCell.csv
    │   ├── Basel_Zuri_StainingPanel.csv
    │   ├── Basel_Zuri_WholeImage.csv
    │   └── Zuri_PatientMetadata.csv
    ├── Basel_Zuri_masks/
    │   └── *.tiff (746 files)
    └── ome/
        └── *.tiff (746 files)
        
The Data
====

The data, from the B. Bodenmiller lab, is a collection of images acquired with Imaging Mass Citometry of breast cancer cells of different patients and under different conditions [1]_.
Each ``.tiff`` file in the ``ome`` folder is uniquely paired with a ``.tiff`` mask. Each mask tells which are the cells.

FAQ
====

Q: Is the data showing 2D sections of 3D bodies?

A: No

----

.. [1] Schulz D, Zanotelli VRT, Bodenmiller B. et al. *Simultaneous Multiplexed Imaging of mRNA and Proteins with Subcellular Resolution in Breast Cancer Tissue Samples by Mass Cytometry.* Cell Syst. 2018 Jan 24
