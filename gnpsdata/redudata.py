import pandas as pd

def get_redu_metadata():
    df = pd.read_csv("https://redu.gnps2.org/dump", sep="\t")

    return df


