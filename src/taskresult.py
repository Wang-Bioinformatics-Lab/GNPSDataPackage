import requests
import os
import sys


def determine_result_url(task, result_path):
    url = "https://proteomics2.ucsd.edu/ProteoSAFe/DownloadResultFile?task={}&file={}&block=main".format(task, result_path)

    return url

# This downloads a specific file from a task
def download_task_results(task, result_path, output_file):
    url = determine_result_url(task, result_path)

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(output_file, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
    
    return 