import sys
sys.path.insert(0, '..')

def test_fasst_usi_search():
    print("USI Search")

    from gnpsdata import fasst
    import requests

    usi = "mzspec:GNPS:GNPS-LIBRARY:accession:CCMSLIB00005435899"

    results = fasst.query_fasst_usi(usi, "gnpsdata_index_11_25_23", analog=False, \
                    precursor_mz_tol=0.05, fragment_mz_tol=0.05, min_cos=0.7)

    assert(len(results) > 50)
    

def main():
    test_fasst_usi_search()

if __name__ == "__main__":
    main()
