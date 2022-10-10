import pandas as pd

def get_redu_metadata():
    df = pd.read_csv("https://redu.ucsd.edu/dump", sep="\t")

    return df


