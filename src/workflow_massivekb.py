import taskresult


def download_sptxt(task, output_file):
    taskresult.download_task_results(task, "ambiguity_filtered_overlapping_protein_filtered_spectrum_library_sptxt/ambiguity_filtered_overlapping_protein_filtered_peptide_library.sptxt", output_file)

def variants_dataframe(task):
    path_to_result = "spectrum_library_tsv_splits_merged_enriched/"
    