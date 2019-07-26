from sandbox.folders import single_cell_data_path
from sandbox.csv_to_sqlite3_single_cell import database_single_cell, convert_csv_to_sqlite3_single_cell

rule all:
    input:
         # "snakemake/eda_csv"
         "snakemake/test_vae"
    shell:
         # the rules for which the output files are removed basically act as .PHONY targets
         "rm snakemake/*"

rule clean:
    shell:
         "rm snakemake/*"

rule eda_csv:
    output:
          "snakemake/eda_csv"
    shell:
         """
         python3 -m sandbox.csv_parser
         # can dependencies be specified without having to deal with files?
         mkdir -p snakemake; touch snakemake/eda_csv
         """

rule eda_ome:
    output:
          "snakemake/eda_ome"
    shell:
         """
         python3 -m sandbox.misc
         mkdir -p snakemake; touch snakemake/eda_ome
         """

rule csv_to_sqlite3_single_cell:
    input:
         single_cell_data_path
    output:
          database_single_cell
    run:
        convert_csv_to_sqlite3_single_cell()

rule test_vae:
    input:
         database_single_cell
    output:
          "snakemake/test_vae"
    shell:
         """
         python3 -m sandbox.vae
         mkdir -p snakemake; touch snakemake/test_vae
         """
