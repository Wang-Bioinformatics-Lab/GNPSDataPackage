import sys
sys.path.insert(0, '..')

def test_massivekb_sptxt():
    task = "82c0124b6053407fa41ba98f53fd8d89"
    result_path = "ambiguity_filtered_overlapping_protein_filtered_spectrum_library_sptxt/ambiguity_filtered_overlapping_protein_filtered_peptide_library.sptxt"

    from gnpsdata import taskresult

    taskresult.download_task_resultfile(task, result_path, "test.txt", gnps2=False)

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

    workflow_classicnetworking.download_graphml(task, "temp.graphml", gnps2=False)
    workflow_classicnetworking.get_graphml_network(task)

def test_fbmn_graphml():
    from gnpsdata import workflow_fbmn

    task = "5f49ed8f3963479995cc48a239cd205d"

    workflow_fbmn.download_graphml(task, "temp.graphml", gnps2=False)
    workflow_fbmn.get_graphml_network(task)
    
def test_dashboard():
    from gnpsdata import dashboard

    url = dashboard.get_dashboard_viewer_linkout("mzspec:MSV000085852:QC_0",
        xic_mz=None,
        xic_rt=None,
        ms2_scan=None)
    
    print(url)

# These are the GNPS2 tests
def test_gnps2_task_result():
    from gnpsdata import taskresult

    taskresult.download_gnps2_task_resultfile("b8e2a2c89f924a5d8bef4ab3c5c90937", "gnps_network/network.graphml", "network.graphml")

def test_public_dataset():
    from gnpsdata import publicdata

    all_files = publicdata.get_massive_public_dataset_filelist("MSV000086709")
    
    print(len(all_files))

    assert(len(all_files) > 15)

def test_fasst_usi_search():
    print("USI Search")

    from gnpsdata import fasst
    import requests

    usi = "mzspec:MSV000083540:ccms_peak/Pooled_Urine_5_posneg_b.mzML:scan:5443"

    results = fasst.query_fasst_usi(usi, "gnpsdata_index")
    assert(len(results["results"]) > 1000)


def test_fasst_peaks_search():
    from gnpsdata import fasst
    import requests

    print("USI Search by Peaks")
    # getting peaks
    usi = "mzspec:MSV000083540:ccms_peak/Pooled_Urine_5_posneg_b.mzML:scan:5443"
    json_spectrum = requests.get("https://metabolomics-usi.gnps2.org/json/?usi1={}".format(usi)).json()

    #url = "http://localhost:5054/"
    url = "https://fasst.gnps2.org/"

    database = "gnpsdata_index"
    
    results = fasst.query_fasst_peaks(json_spectrum["precursor_mz"], json_spectrum["peaks"], database, serverurl=url)

    assert(len(results["results"]) > 1000)

def main():
    #test_massql_conversion()
    #test_classicnetworking_graphml()
    #test_dashboard()
    #test_gnps2_task_result()
    #test_public_dataset()
    #test_fasst_usi_search()
    test_fasst_peaks_search()

if __name__ == "__main__": 
    main()