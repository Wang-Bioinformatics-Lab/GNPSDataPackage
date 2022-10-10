import taskresult


def download_sptxt(task, output_file):
    taskresult.download_task_resultfile(task, "ambiguity_filtered_overlapping_protein_filtered_spectrum_library_sptxt/ambiguity_filtered_overlapping_protein_filtered_peptide_library.sptxt", output_file)

def variants_dataframe(task):
    path_to_result = "spectrum_library_tsv_splits_merged_enriched/"

    return taskresult.get_task_result_dataframe(task, path_to_result)
    