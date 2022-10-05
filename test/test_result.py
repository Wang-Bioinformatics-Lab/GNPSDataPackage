import sys
sys.path.insert(0, '../src')

def test():
    task = "82c0124b6053407fa41ba98f53fd8d89"
    result_path = "ambiguity_filtered_overlapping_protein_filtered_spectrum_library_sptxt/ambiguity_filtered_overlapping_protein_filtered_peptide_library.sptxt"

    import taskresult

    taskresult.download_task_results(task, result_path, "test.txt")
