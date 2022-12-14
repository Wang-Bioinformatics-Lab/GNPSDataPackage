from massql import msql_fileloading
import pandas as pd


def convert_ms_to_feather(input_ms_filename):
    ms1_df, ms2_df = msql_fileloading.load_data(input_ms_filename, cache=True)


def read_ms_data(input_ms_filename):
    ms1_df, ms2_df = msql_fileloading.load_data(input_ms_filename, cache=True)

    return ms1_df, ms2_df

def read_ms_usi(input_file_usi):
    usi = ""
    # TODO: we need to have a resolution in the USI metabolomics resolver to point to the data by url