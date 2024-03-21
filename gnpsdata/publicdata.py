import requests
from bs4 import BeautifulSoup
import json

def get_massive_private_dataset_filelist(accession, username, password):
    url = "https://massive.ucsd.edu/ProteoSAFe/dataset_files.jsp?accession={}".format(accession)

    s = requests.Session()
    payload = {
        'user' : username,
        'password' : password,
        'login' : 'Sign in'
    }

    base_url = "massive.ucsd.edu"

    r = s.post('https://' + base_url + '/ProteoSAFe/user/login.jsp', data=payload, verify=False)

    # Get Data
    r = s.get(url)

    if r.status_code != 200:
        print(r.text)
        raise Exception("Unable to get dataset file list")

    soup = BeautifulSoup(r.text, features="lxml")
    scripts_list = soup.findAll('script')

    files_list = []

    for script in scripts_list:
        if script.string is not None:
            if len(script.string) > 20000:
                print("Lets parse this one")
                new_script = script.string.split("var dataset_files = ")[-1]
                new_script = new_script.split("]};")[0] + "]}"
                files_dict = json.loads(new_script)
                files_list = files_dict["row_data"]

    return files_list


def get_massive_public_dataset_filelist(accession):
    url = "https://massive.ucsd.edu/ProteoSAFe/dataset_files.jsp?accession={}".format(accession)

    # Get Data
    r = requests.get(url)

    if r.status_code != 200:
        print(r.text)
        raise Exception("Unable to get dataset file list")

    soup = BeautifulSoup(r.text, features="lxml")
    scripts_list = soup.findAll('script')

    files_list = []

    for script in scripts_list:
        if script.string is not None:
            if len(script.string) > 500:
                print("Lets parse this script tag")
                new_script = script.string.split("var dataset_files = ")[-1]
                new_script = new_script.split("};")[0] + "}"

                try:
                    files_dict = json.loads(new_script)
                    files_list = files_dict["row_data"]
                except:
                    pass

    return files_list

def get_massive_public_dataset_list():
    all_datasets = []

    # Populating GNPS
    page_size = 1000
    offset = 0

    while True:
        url = "https://massive.ucsd.edu/ProteoSAFe/QueryDatasets?pageSize={}&offset={}&query=%23%7B%22query%22%3A%7B%7D%2C%22table_sort_history%22%3A%22createdMillis_dsc%22%7D".format(page_size, offset)
        r = requests.get(url)

        try:
            r.raise_for_status()
        except:
            break

        dataset_list = r.json()["row_data"]

        if len(dataset_list) < 1:
            break

        print("DONE", dataset_list[0]["dataset"])

        for dataset in dataset_list:
            accession = dataset["dataset"]
            all_datasets.append(dataset)        

        offset += page_size

    return all_datasets