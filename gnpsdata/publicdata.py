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
            if len(script.string) > 20000:
                print("Lets parse this one")
                new_script = script.string.split("var dataset_files = ")[-1]
                new_script = new_script.split("]};")[0] + "]}"
                files_dict = json.loads(new_script)
                files_list = files_dict["row_data"]

    return files_list