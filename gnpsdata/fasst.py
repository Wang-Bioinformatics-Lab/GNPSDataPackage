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
                    lower_delta=100, upper_delta=200):
    params = {
        "usi": usi,
        "library": database,
        "analog": "Yes" if analog else "No",
        "upper_delta": upper_delta,
        "lower_delta": lower_delta,
        "pm_tolerance": precursor_mz_tol,
        "fragment_tolerance": fragment_mz_tol,
        "cosine_threshold": min_cos,
        "cache": "No"
    }

    r = requests.get(os.path.join(host, "search"), params=params, timeout=50)
    r.raise_for_status()

    return r.json()

# high performance version
def query_fasst_api_usi(usi, database, host="https://api.fasst.gnps2.org",
                    analog=False, precursor_mz_tol=0.05,
                    fragment_mz_tol=0.05, min_cos=0.7,
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
    
    params["task_id"] = task_id
    params["status"] = "PENDING"

    if blocking is False:
        return params

    return get_results(params, host=host)

def query_fasst_peaks(precursor_mz, peaks, database, host="https://fasst.gnps2.org", \
        analog=False, \
        precursor_mz_tol=0.05, fragment_mz_tol=0.05, min_cos=0.7):
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

    params["task_id"] = task_id
    params["status"] = "PENDING"
    
    if blocking is False:
        return params

    return get_results(params, host=host)


IN_FLIGHT_STATUSES = {"PENDING", "RUNNING", "STARTED", "RETRY"}

def get_results(query_parameters_dictionary, host="https://api.fasst.gnps2.org", blocking=True):
    task_id = query_parameters_dictionary["task_id"]

    retries_max = 120
    current_retries = 0
    while True:
        print("WAITING FOR RESULTS", current_retries, task_id)

        r = requests.get(os.path.join(host, "search/result/{}".format(task_id)), timeout=30)

        try:
            r.raise_for_status()
        except KeyboardInterrupt:
            raise
        except:
            # if we are not blocking, we just return the status
            if blocking is False:
                return "PENDING"

            time.sleep(1)
            current_retries += 1


            continue

        response_json = r.json()

        # checking if the results are ready
        if "status" in response_json and response_json["status"] in IN_FLIGHT_STATUSES:
            # if we are not blocking, we just return the status
            if blocking is False:
                return response_json["status"]

            time.sleep(1)
            current_retries += 1

            if current_retries >= retries_max:
                raise Exception("Timeout waiting for results from FASST API")

            continue

        if "results" not in response_json:
            raise ValueError("Unexpected FASST API response, missing 'results' key: {}".format(response_json))

        return response_json

def get_databases(host="https://fasst.gnps2.org"):
    url = "{}/libraries".format(host)

    return requests.get(url).json()
