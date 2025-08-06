import pandas as pd
import argparse
import os
import json
import requests
import time
from tqdm import tqdm

# this is sychronous low performance
def query_fasst_usi(usi, database, host="https://fasst.gnps2.org",
                    analog=False, precursor_mz_tol=0.05,
                    fragment_mz_tol=0.05, min_cos=0.7,
                    cache="Yes"):
    params = {
        "usi": usi,
        "library": database,
        "analog": "Yes" if analog else "No",
        "pm_tolerance": precursor_mz_tol,
        "fragment_tolerance": fragment_mz_tol,
        "cosine_threshold": min_cos,
        "cache": cache
    }

    r = requests.get(os.path.join(host, "search"), params=params, timeout=50)
    r.raise_for_status()

    return r.json()

# high performance version
def query_fasst_api_usi(usi, database, host="https://api.fasst.gnps2.org",
                    analog=False, precursor_mz_tol=0.05,
                    fragment_mz_tol=0.05, min_cos=0.7,
                    cache="Yes",
                    lower_delta=100,
                    upper_delta=100,
                    blocking=True):
    
    params = {
        "library": database,
        "usi": usi,
        "analog": "Yes" if analog else "No",
        "cache": "No",
        "lower_delta": lower_delta,
        "upper_delta": upper_delta,
        "pm_tolerance": precursor_mz_tol,
        "fragment_tolerance": fragment_mz_tol,
        "cosine_threshold": min_cos
    }


    r = requests.post(os.path.join(host, "search"), json=params, timeout=5)
    r.raise_for_status()

    task_id = r.json()["id"]
    
    if blocking is False:
        params["task_id"] = task_id
        params["status"] = "PENDING"

        return params
    
    return blocking_for_results(params, host=host)

def query_fasst_peaks(precursor_mz, peaks, database, host="https://fasst.gnps2.org", analog=False, precursor_mz_tol=0.05, fragment_mz_tol=0.05, min_cos=0.7):
    spectrum_query = {
        "peaks": peaks,
        "precursor_mz": precursor_mz
    }

    params = {
        "query_spectrum": json.dumps(spectrum_query),
        "library": database,
        "analog": "Yes" if analog else "No",
        "pm_tolerance": precursor_mz_tol,
        "fragment_tolerance": fragment_mz_tol,
        "cosine_threshold": min_cos,
    }

    r = requests.post(os.path.join(host, "search"), data=params, timeout=50)

    r.raise_for_status()

    return r.json()



def query_fasst_api_peaks(precursor_mz, peaks, database, 
                          host="https://api.fasst.gnps2.org", 
                          analog=False, precursor_mz_tol=0.05, 
                          fragment_mz_tol=0.05, 
                          min_cos=0.7, 
                          lower_delta=100,
                          upper_delta=100,
                          blocking=True):
    spectrum_query = {
        "peaks": peaks,
        "precursor_mz": precursor_mz
    }

    params = {
        "library": database,
        "query_spectrum": json.dumps(spectrum_query),
        "analog": "Yes" if analog else "No",
        "cache": "No",
        "lower_delta": lower_delta,
        "upper_delta": upper_delta,
        "pm_tolerance": precursor_mz_tol,
        "fragment_tolerance": fragment_mz_tol,
        "cosine_threshold": min_cos
    }

    query_url = os.path.join(host, "search")

    r = requests.post(query_url, json=params, timeout=5)
    
    r.raise_for_status()

    task_id = r.json()["id"]
    
    if blocking is False:
        params["task_id"] = task_id
        params["status"] = "PENDING"

        return params
    
    return blocking_for_results(params, host=host)


def blocking_for_results(query_parameters_dictionary, host="https://api.fasst.gnps2.org"):
    task_id = query_parameters_dictionary["task_id"]
    
    retries_max = 120
    current_retries = 0
    while True:
        print("WAITING FOR RESULTS", current_retries, task_id)
        
        r = requests.get(os.path.join(host, "search/result/{}".format(task_id)), timeout=30)

        r.raise_for_status()

        # checking if the results are ready
        if "status" in r.json() and r.json()["status"] == "PENDING":
            time.sleep(1)
            current_retries += 1

            if current_retries >= retries_max:
                raise Exception("Timeout waiting for results from FASST API")
            
            continue
    
        return r.json()

def get_databases(host="https://fasst.gnps2.org"):
    url = "{}/libraries".format(host)

    return requests.get(url).json()