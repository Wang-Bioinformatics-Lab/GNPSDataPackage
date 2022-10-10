import requests
import os
import sys
import pandas as pd

def determine_result_file_url(task, result_path):
    url = "https://proteomics2.ucsd.edu/ProteoSAFe/DownloadResultFile?task={}&file={}&block=main".format(task, result_path)

    return url

def determine_resultview_file_url(task, result_view_name):
    # Workflow Type
    status_url = "https://gnps.ucsd.edu/ProteoSAFe/QueryTaskDetails?task={}".format(task)
    r = requests.get(status_url)
    workflow_name = r.json()["workflow"]
    workflow_version = r.json()["workflow_version"]
    site = r.json()["site"]
    site_url = "https://gnps.ucsd.edu"

    if "BETA" in site:
        site_url = "https://proteomics2.ucsd.edu"

    # Getting the workflow specification
    try:
        workflow_spec_url = "{}/ProteoSAFe/DownloadWorkflowInterface?workflow={}&type=result&version={}".format(site_url, workflow_name, workflow_version)
        r = requests.get(workflow_spec_url)
        r.raise_for_status()
    except:
        raise

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(r.text, 'html.parser')

    # Finding the view id
    block_id = None
    for view_div in soup.find_all("view"):
        view_id = view_div["id"]

        if view_id == result_view_name:
            for child in view_div.descendants:
                try:
                    block_id = child["type"]
                except:
                    pass

    file_path = None
    for block in soup.find_all("block"):
        my_block_id = block["id"]

        if my_block_id == block_id:
            file_path = block.find_all("source")[0]["name"]

    url = "https://proteomics2.ucsd.edu/ProteoSAFe/DownloadResultFile?task={}&file={}&block=main".format(task, file_path)

    return url


# This downloads a specific file from a task
def download_task_resultfile(task, result_path, output_file):
    url = determine_result_file_url(task, result_path)

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(output_file, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
    
    return

def download_task_resultview(task, result_view, output_file):
    url = determine_resultview_file_url(task, result_view)

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(output_file, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
    
    return 

def get_task_result_dataframe(task, result_path):
    url = determine_result_file_url(task, result_path)

    df = pd.read_csv(url, sep="\t")

    return df

def get_task_resultview_dataframe(task, result_view_name):
    url = determine_resultview_file_url(task, result_view_name)

    df = pd.read_csv(url, sep="\t")

    return df