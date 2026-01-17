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
                    precursor_mz_tol=0.05, fragment_mz_tol=0.05, min_cos=0.7)


    assert(len(results["results"]) > 50)


    usi = "mzspec:GNPS:GNPS-LIBRARY:accession:CCMSLIB00005435899"

    results = fasst.query_fasst_usi(usi, "metabolomicspanrepo_index_latest", host=FASST_SERVER_URL, analog=False, \
                    precursor_mz_tol=0.05, fragment_mz_tol=0.05, min_cos=0.7)


    assert(len(results["results"]) > 50)


    # TODO: Testing the results to resolve the MS/MS on them

    print(results["results"][0])

def test_fasst_api_usi_search():
    print("USI Search API")

    from gnpsdata import fasst

    usi = "mzspec:GNPS:GNPS-LIBRARY:accession:CCMSLIB00005435899"

    results = fasst.query_fasst_api_usi(usi, "metabolomicspanrepo_index_nightly", host=FASST_API_SERVER_URL, analog=False, \
                    precursor_mz_tol=0.05, fragment_mz_tol=0.05, min_cos=0.7)

    assert(len(results["results"]) > 50)

    usi = "mzspec:GNPS:GNPS-LIBRARY:accession:CCMSLIB00005435899"

    results = fasst.query_fasst_api_usi(usi, "metabolomicspanrepo_index_latest", host=FASST_API_SERVER_URL, analog=False, \
                    precursor_mz_tol=0.05, fragment_mz_tol=0.05, min_cos=0.7)

    assert(len(results["results"]) > 50)

    usi = "mzspec:GNPS:GNPS-LIBRARY:accession:CCMSLIB00000078211"

    results = fasst.query_fasst_usi(usi, "metabolomicspanrepo_index_latest", host=FASST_SERVER_URL, analog=False, \
                    precursor_mz_tol=0.05, fragment_mz_tol=0.05, min_cos=0.7)
    
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
                    precursor_mz_tol=0.05, fragment_mz_tol=0.05, min_cos=0.7, blocking=False)
        
        status_results_list.append(results)

    # lets now wait for all the results to be ready
    for status in status_results_list:
        results = fasst.get_results(status)

def test_throughput_api_search():
    from gnpsdata import fasst

    usi = "mzspec:GNPS:GNPS-LIBRARY:accession:CCMSLIB00005464852" # expensive query
    #usi = "mzspec:GNPS:GNPS-LIBRARY:accession:CCMSLIB00005435899" # cheap query

    status_results_list = []
    for i in range(0, 20):
        print("submitted", i)
        results = fasst.query_fasst_api_usi(usi, "metabolomicspanrepo_index_nightly", host=FASST_API_SERVER_URL, analog=False, \
                    precursor_mz_tol=0.05, fragment_mz_tol=0.05, min_cos=0.7, blocking=False)
        
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

def test_big_analog_api_search():
    from gnpsdata import fasst

    usi = "mzspec:GNPS:MONA:accession:CCMSLIB00006685129"

    results = fasst.query_fasst_api_usi(usi, "metabolomicspanrepo_index_nightly", host=FASST_API_SERVER_URL, analog=True, \
                    precursor_mz_tol=0.1, fragment_mz_tol=0.1, min_cos=0.7)

    print("Total Analog Hits", len(results["results"]))

def test_yasin_incomplete_api_search():
    from gnpsdata import fasst

    usi = "mzspec:GNPS:GNPS-LIBRARY:accession:CCMSLIB00003140022"

    results = fasst.query_fasst_api_usi(usi, "metabolomicspanrepo_index_nightly", host=FASST_API_SERVER_URL, analog=False, \
                    precursor_mz_tol=0.05, fragment_mz_tol=0.05, min_cos=0.7)

    print("Total Hits", len(results["results"]))

    # This USI should be in the results "mzspec:MSV000095418:peak/20240502_U19_ADRC_Main_SetOne_mzML/U19_ADRC_Main_mzML/P3_A12_6001897.mzML:scan:1356"
    import pandas as pd
    results_df = pd.DataFrame(results["results"])

    assert ("mzspec:MSV000095418:peak/20240502_U19_ADRC_Main_SetOne_mzML/U19_ADRC_Main_mzML/P3_A12_6001897.mzML:scan:1356" in results_df["USI"].values)

    assert ("MSV000095418" in results_df["Dataset"].values)

    # Shoudl be more than 7K results
    assert (len(results["results"]) > 7000)


def test_yasin_analog_api_search():
    usi = "mzspec:GNPS:GNPS-LIBRARY:accession:CCMSLIB00016217549"

    from gnpsdata import fasst

    results = fasst.query_fasst_api_usi(usi, "metabolomicspanrepo_index_nightly", host=FASST_API_SERVER_URL, analog=True, \
                    precursor_mz_tol=0.1, fragment_mz_tol=0.1, min_cos=0.7, lower_delta=70,
                    upper_delta=70, blocking=True)
    
    print("Total Analog Hits", len(results["results"]))

def debug_yasin_large_analog_api_search():
    from gnpsdata import fasst
    import pandas as pd

    usi_df = pd.read_csv("data/test_usis.tsv")  

    print("Total USIs to test:", len(usi_df))

    status_results_list = []
    for index, row in usi_df.iterrows():
        usi = row["usi"]

        print("Testing USI:", usi)

        results = fasst.query_fasst_api_usi(usi, "metabolomicspanrepo_index_nightly", host=FASST_API_SERVER_URL, analog=True, \
                        precursor_mz_tol=0.1, fragment_mz_tol=0.1, min_cos=0.7, lower_delta=70,
                        upper_delta=70, blocking=False)
        
        status_results_list.append([results, usi])
    
    # now lets wait and get the results
    # lets now wait for all the results to be ready
    time.sleep(1)
    for k in range(0, 180):
        all_results_finished = True
        count_finished = 0
        for i, result_entry in enumerate(status_results_list):
            status = result_entry[0]
            usi = result_entry[1]
            if status["status"] == "DONE" or status["status"] == "TIMEOUT":
                count_finished += 1
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
                print("Error Results for", usi)
                continue

        if all_results_finished:
            break
        print("Finished so far:", count_finished, "out of", len(status_results_list))
        time.sleep(5)

    # Initialize a dictionary to hold the counts
    counts = {
        "DONE": 0, 
        "PENDING": 0, 
        "ERROR": 0, 
        "UNKNOWN": 0
    }

    # Summarizing the results
    for i, result_entry in enumerate(status_results_list):
        status = result_entry[0]
        usi = result_entry[1]

        current_status = status["status"]
        
        if current_status == "DONE":
            counts["DONE"] += 1
            print("Total Hits", len(status["results"]))
        elif current_status == "PENDING":
            counts["PENDING"] += 1
            print("Pending Results")
        elif current_status == "ERROR":
            counts["ERROR"] += 1
            print("Error in Results")
        else:
            counts["UNKNOWN"] += 1
            print("Unknown Status", current_status)

    # Print the final tally
    print("-" * 20)
    print("Final Counts:")
    print(f"DONE:    {counts['DONE']}")
    print(f"PENDING: {counts['PENDING']}")
    print(f"ERROR:   {counts['ERROR']}")
    print(f"UNKNOWN: {counts['UNKNOWN']}")
    
        


def test_libraries_list():
    url = "{}/libraries".format(FASST_SERVER_URL)

    from gnpsdata import fasst
    
    libraries = fasst.get_databases(host=FASST_SERVER_URL)

    print(libraries)

    assert(len(libraries) > 0)

def debug_local():
    usi = "mzspec:GNPS:GNPS-LIBRARY:accession:CCMSLIB00003140022"

    from gnpsdata import fasst

    results = fasst.query_fasst_api_usi(usi, "gnpslibrary", host="http://localhost:5055", analog=False, \
                    precursor_mz_tol=0.05, fragment_mz_tol=0.05, min_cos=0.7)

    print(results)


def main():
    #test_fasst_usi_search()
    #test_fasst_api_usi_search()
    #test_fasst_api_peaks_search()
    #test_fasst_api_search_nonblocking()
    #test_throughput_api_search()
    #test_big_analog_api_search()
    #test_yasin_incomplete_api_search()
    #test_yasin_analog_api_search()
    debug_yasin_large_analog_api_search()
    
    #test_libraries_list()

    #debug_local()

if __name__ == "__main__":
    main()
