import sys
import requests
sys.path.insert(0, '..')
sys.path.insert(0, '../modules/GNPSDataPackage/')

FASST_SERVER_URL = "https://fasst.gnps2.org"
FASST_API_SERVER_URL = "https://api.fasst.gnps2.org"
#FASST_SERVER_URL = "http://169.235.26.140:5054"

def test_fasst_usi_search():
    print("USI Search")

    from gnpsdata import fasst

    usi = "mzspec:GNPS:GNPS-LIBRARY:accession:CCMSLIB00005435899"

    results = fasst.query_fasst_usi(usi, "metabolomicspanrepo_index_nightly", host=FASST_SERVER_URL, analog=False, \
                    precursor_mz_tol=0.05, fragment_mz_tol=0.05, min_cos=0.7, cache="No")


    assert(len(results["results"]) > 50)


    usi = "mzspec:GNPS:GNPS-LIBRARY:accession:CCMSLIB00005435899"

    results = fasst.query_fasst_usi(usi, "metabolomicspanrepo_index_latest", host=FASST_SERVER_URL, analog=False, \
                    precursor_mz_tol=0.05, fragment_mz_tol=0.05, min_cos=0.7, cache="No")


    assert(len(results["results"]) > 50)

    # TODO: Testing the results to resolve the MS/MS on them

    print(results["results"][0])

def test_fasst_api_usi_search():
    print("USI Search API")

    from gnpsdata import fasst

    usi = "mzspec:GNPS:GNPS-LIBRARY:accession:CCMSLIB00005435899"

    results = fasst.query_fasst_api_usi(usi, "metabolomicspanrepo_index_nightly", host=FASST_API_SERVER_URL, analog=False, \
                    precursor_mz_tol=0.05, fragment_mz_tol=0.05, min_cos=0.7, cache="No")

    assert(len(results["results"]) > 50)

    usi = "mzspec:GNPS:GNPS-LIBRARY:accession:CCMSLIB00005435899"

    results = fasst.query_fasst_api_usi(usi, "metabolomicspanrepo_index_latest", host=FASST_API_SERVER_URL, analog=False, \
                    precursor_mz_tol=0.05, fragment_mz_tol=0.05, min_cos=0.7, cache="No")

    assert(len(results["results"]) > 50)

def test_libraries_list():
    url = "{}/libraries".format(FASST_SERVER_URL)

    from gnpsdata import fasst
    
    libraries = fasst.get_databases(host=FASST_SERVER_URL)

    print(libraries)

    assert(len(libraries) > 0)

def main():
    #test_fasst_usi_search()
    test_fasst_api_usi_search()
    #test_libraries_list()

if __name__ == "__main__":
    main()
