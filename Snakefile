rule all:
    input:
        "snakemake/eda_csv", "snakemake/eda_ome"

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
