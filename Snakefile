from sandbox.folders import basel_patient_data_path, \
    zurich_patient_data_path, \
    single_cell_data_path, \
    staining_data_path, \
    whole_image_data_path

from sandbox.csv_parser import result_path_from_csv_path

small_csv_files = [basel_patient_data_path, zurich_patient_data_path, staining_data_path, whole_image_data_path]
small_csv_files_output = [result_path_from_csv_path(f) for f in small_csv_files]

rule eda_small_csvs:
    input:
         csv_files=small_csv_files,
         source_code="sandbox/csv_parser.py"
    output:
          small_csv_files_output
    shell:
         "python3 -m sandbox.csv_parser {input.csv_files}"

# rule eda_large_csv:
#     input:
#          csv_file=single_cell_data_path,
#          source_code='sandbox/csv_parser.py'
#     output:
#           result_path_from_csv_path(single_cell_data_path)
#     shell:
#          "python3 -m sandbox.csv_parser {input.csv_file}"
