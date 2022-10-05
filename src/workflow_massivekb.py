import taskresult


def download_sptxt(task, output_file):
    taskresult.download_task_results(task, "ambiguity_filtered_overlapping_protein_filtered_spectrum_library_sptxt/ambiguity_filtered_overlapping_protein_filtered_peptide_library.sptxt", output_file)

