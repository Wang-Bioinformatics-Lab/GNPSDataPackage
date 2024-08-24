import sys
sys.path.insert(0, '..')
sys.path.insert(0, '../modules/GNPSDataPackage/')

def test_fasst_usi_search():
    print("USI Search")

    from gnpsdata import fasst

    usi = "mzspec:GNPS:GNPS-LIBRARY:accession:CCMSLIB00005435899"

    host="https://fasst.gnps2.org/search"
    #host="http://169.235.26.140:5054/search"

    results = fasst.query_fasst_usi(usi, "gnpsdata_index_11_25_23", host=host, analog=False, \
                    precursor_mz_tol=0.05, fragment_mz_tol=0.05, min_cos=0.7, cache="No")


    assert(len(results["results"]) > 50)

    # TODO: Testing the results to resolve the MS/MS on them

def main():
    test_fasst_usi_search()

if __name__ == "__main__":
    main()
