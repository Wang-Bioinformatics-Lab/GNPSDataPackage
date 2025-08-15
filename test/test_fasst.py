import sys
import requests
import time
sys.path.insert(0, '..')
sys.path.insert(0, '../modules/GNPSDataPackage/')

FASST_SERVER_URL = "https://fasst.gnps2.org"
FASST_API_SERVER_URL = "https://api.fasst.gnps2.org"
#FASST_API_SERVER_URL = "http://localhost:5055"

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

    usi = "mzspec:GNPS:GNPS-LIBRARY:accession:CCMSLIB00000078211"

    results = fasst.query_fasst_usi(usi, "metabolomicspanrepo_index_latest", host=FASST_SERVER_URL, analog=False, \
                    precursor_mz_tol=0.05, fragment_mz_tol=0.05, min_cos=0.7, cache="No")
    
    print(results)

def test_fasst_api_peaks_search():
    print("Peaks Search API")

    from gnpsdata import fasst
    import json

    peaks_from_resolver = json.loads(open("data/test_peaks_resolver.json", "r").read())

    database = "metabolomicspanrepo_index_nightly"

    results = fasst.query_fasst_api_peaks(peaks_from_resolver["precursor_mz"], peaks_from_resolver["peaks"], database, host=FASST_API_SERVER_URL, analog=False, \
                    precursor_mz_tol=0.05, fragment_mz_tol=0.05, min_cos=0.7)

    print(results)


def test_fasst_api_search_nonblocking():
    from gnpsdata import fasst

    usi = "mzspec:GNPS:GNPS-LIBRARY:accession:CCMSLIB00005435899"

    status_results_list = []
    for i in range(0, 10):
        print("submitted", i)
        results = fasst.query_fasst_api_usi(usi, "metabolomicspanrepo_index_nightly", host=FASST_API_SERVER_URL, analog=False, \
                    precursor_mz_tol=0.05, fragment_mz_tol=0.05, min_cos=0.7, cache="No", blocking=False)
        
        status_results_list.append(results)

    # lets now wait for all the results to be ready
    for status in status_results_list:
        results = fasst.get_results(status)

def test_throughput_api_search():
    from gnpsdata import fasst

    usi = "mzspec:GNPS:GNPS-LIBRARY:accession:CCMSLIB00005464852" # expensive query
    #usi = "mzspec:GNPS:GNPS-LIBRARY:accession:CCMSLIB00005435899" # cheap query

    status_results_list = []
    for i in range(0, 100):
        print("submitted", i)
        results = fasst.query_fasst_api_usi(usi, "metabolomicspanrepo_index_nightly", host=FASST_API_SERVER_URL, analog=False, \
                    precursor_mz_tol=0.05, fragment_mz_tol=0.05, min_cos=0.7, cache="Yes", blocking=False)
        
        status_results_list.append(results)

    # lets now wait for all the results to be ready
    time.sleep(1)
    for k in range(0, 60):
        all_results_finished = True
        for i, status in enumerate(status_results_list):
            if status["status"] == "DONE" or status["status"] == "TIMEOUT":
                continue
            
            # checking on the results
            all_results_finished = False
            try:
                results = fasst.get_results(status, blocking=False)
                if results == "PENDING":
                    status["status"] = "PENDING"
                    print("Pending Results for", i)
                    continue
                else:
                    status["status"] = "DONE"
                    status["results"] = results["results"]
            except:
                status["status"] = "ERROR"
                continue

        if all_results_finished:
            break
        time.sleep(5)

    # summarizing the results
    for status in status_results_list:
        if status["status"] == "DONE":
            print("Total Hits", len(status["results"]))
        elif status["status"] == "PENDING":
            print("Pending Results")
        elif status["status"] == "ERROR":
            print("Error in Results")
        else:
            print("Unknown Status", status["status"])

    # for status in status_results_list:
    #     results = fasst.blocking_for_results(status)

    #     try:
    #         print("Total Analog Hits", len(results["results"]))
    #     except KeyError:
    #         print(results)


def test_libraries_list():
    url = "{}/libraries".format(FASST_SERVER_URL)

    from gnpsdata import fasst
    
    libraries = fasst.get_databases(host=FASST_SERVER_URL)

    print(libraries)

    assert(len(libraries) > 0)

def main():
    #test_fasst_usi_search()
    #test_fasst_api_usi_search()
    #test_fasst_api_peaks_search()
    #test_fasst_api_search_nonblocking()
    test_throughput_api_search()
    
    #test_libraries_list()

if __name__ == "__main__":
    main()
