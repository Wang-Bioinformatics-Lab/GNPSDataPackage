import requests

def xic_fast(precursor_mz, rt, database):
    url = "https://xic.gnps2.org/api/integrate/{}".format(database)
    params = {
        "xictarget": precursor_mz,
        "rtrange": rt,
    }

    r = requests.get(url, params=params)

    return r.json()
