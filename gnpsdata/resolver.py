import requests

# This goes to resolver and gets the peaks
def resolve_usi(usi):
    url = "https://metabolomics-usi.gnps2.org/json/"

    params = {}
    params["usi"] = usi

    r = requests.get(url, params=params)

    r.raise_for_status()

    return r.json()