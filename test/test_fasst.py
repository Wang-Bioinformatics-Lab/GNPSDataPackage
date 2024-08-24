import sys
import requests
sys.path.insert(0, '..')
sys.path.insert(0, '../modules/GNPSDataPackage/')

FASST_SERVER_URL = "https://fasst.gnps2.org"
#FASST_SERVER_URL = "http://169.235.26.140:5054"

def test_fasst_usi_search():
    print("USI Search")

    from gnpsdata import fasst

    usi = "mzspec:GNPS:GNPS-LIBRARY:accession:CCMSLIB00005435899"

    results = fasst.query_fasst_usi(usi, "gnpsdata_index_11_25_23", host=FASST_SERVER_URL, analog=False, \
                    precursor_mz_tol=0.05, fragment_mz_tol=0.05, min_cos=0.7, cache="No")


    assert(len(results["results"]) > 50)

    # TODO: Testing the results to resolve the MS/MS on them

    print(results["results"][0])

def test_fasst_usi_search_mtbls():
    print("USI Search")

    from gnpsdata import fasst

    usi = "mzspec:MSV000083540:ccms_peak/Pooled_Urine_5_posneg_b.mzML:scan:5443"

    results = fasst.query_fasst_usi(usi, "mtbls_7_23_24", host=FASST_SERVER_URL, analog=False, \
                    precursor_mz_tol=0.05, fragment_mz_tol=0.05, min_cos=0.7, cache="No")


    assert(len(results["results"]) > 50)

    print(results["results"][0])


def test_libraries_list():
    url = "{}/libraries".format(FASST_SERVER_URL)

    from gnpsdata import fasst
    
    libraries = fasst.get_databases(host=FASST_SERVER_URL)

    print(libraries)

    assert(len(libraries) > 0)

def main():
    #test_fasst_usi_search()
    test_fasst_usi_search_mtbls()
    #test_libraries_list()

if __name__ == "__main__":
    main()
