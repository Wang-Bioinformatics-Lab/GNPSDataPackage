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

    print(os.path.join(host, "search"))

    r = requests.get(os.path.join(host, "search"), params=params, timeout=50)

    r.raise_for_status()

    print(r.json())

    task_id = r.json()["id"]
    
    # now we will wait and then get the results
    while True:
        time.sleep(1)
        r = requests.post(os.path.join(host, "search/result/{}".format(task_id)), timeout=50)

        r.raise_for_status()

        return r.json()


    return r.json()

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


def get_databases(host="https://fasst.gnps2.org"):
    url = "{}/libraries".format(host)

    return requests.get(url).json()