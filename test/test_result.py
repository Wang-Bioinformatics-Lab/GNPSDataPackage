import sys
sys.path.insert(0, '../src')

def test_massivekb_sptxt():
    task = "82c0124b6053407fa41ba98f53fd8d89"
    result_path = "ambiguity_filtered_overlapping_protein_filtered_spectrum_library_sptxt/ambiguity_filtered_overlapping_protein_filtered_peptide_library.sptxt"

    import taskresult

    taskresult.download_task_resultfile(task, result_path, "test.txt")

def test_task_resultview():
    task = "471e71b94f6945ae8a007b0f7b0dbc4e"
    result_view = "view_results"

    import taskresult

    url = taskresult.determine_resultview_file_url(task, result_view)
    df = taskresult.get_task_resultview_dataframe(task, result_view)

    assert(len(df) > 0)

    print(df)
    
def test_massql_conversion():
    import msdata

    msdata.convert_ms_to_feather("test.mzML", "test")


def main():
    test_massql_conversion()


if __name__ == "__main__": 
    main()