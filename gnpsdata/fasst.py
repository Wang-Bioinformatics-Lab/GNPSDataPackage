import pandas as pd
import argparse
import json
import requests
import requests_cache
from tqdm import tqdm
#requests_cache.install_cache('demo_cache')

def query_fasst_usi(usi, database, analog=False, precursor_mz_tol=0.05, fragment_mz_tol=0.05, min_cos=0.7):
    URL = "https://fasst.gnps2.org/search"

    params = {
        "usi": usi,
        "library": database,
        "analog": "Yes" if analog else "No",
        "pm_tolerance": precursor_mz_tol,
        "fragment_tolerance": fragment_mz_tol,
        "cosine_threshold": min_cos,
    }

    r = requests.get(URL, params=params, timeout=50)
    r.raise_for_status()

    return r.json()

def query_fasst_peaks(precursor_mz, peaks, database, serverurl="https://fasst.gnps2.org/", analog=False, precursor_mz_tol=0.05, fragment_mz_tol=0.05, min_cos=0.7):
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

    r = requests.post(serverurl + "search", data=params, timeout=50)

    r.raise_for_status()

    return r.json()