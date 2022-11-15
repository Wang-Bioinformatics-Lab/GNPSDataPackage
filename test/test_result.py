import sys
sys.path.insert(0, '..')

def test_massivekb_sptxt():
    task = "82c0124b6053407fa41ba98f53fd8d89"
    result_path = "ambiguity_filtered_overlapping_protein_filtered_spectrum_library_sptxt/ambiguity_filtered_overlapping_protein_filtered_peptide_library.sptxt"

    from gnpsdata import taskresult

    taskresult.download_task_resultfile(task, result_path, "test.txt")

def test_task_resultview():
    task = "471e71b94f6945ae8a007b0f7b0dbc4e"
    result_view = "view_results"

    from gnpsdata import taskresult

    url = taskresult.determine_resultview_file_url(task, result_view)
    df = taskresult.get_task_resultview_dataframe(task, result_view)

    assert(len(df) > 0)

    print(df)

def test_massql_conversion():
    from gnpsdata import msdata

    msdata.convert_ms_to_feather("data/DSM_17855_SI-1.mzML")

def test_classicnetworking_graphml():
    from gnpsdata import workflow_classicnetworking

    task = "78a99abcdbe94d69a6d1b392848ed052"

    workflow_classicnetworking.download_graphml(task, "temp.graphml")
    workflow_classicnetworking.get_graphml_network(task)

def test_fbmn_graphml():
    from gnpsdata import workflow_fbmn

    task = "5f49ed8f3963479995cc48a239cd205d"

    workflow_fbmn.download_graphml(task, "temp.graphml")
    workflow_fbmn.get_graphml_network(task)
    
def main():
    #test_massql_conversion()
    test_classicnetworking_graphml()


if __name__ == "__main__": 
    main()