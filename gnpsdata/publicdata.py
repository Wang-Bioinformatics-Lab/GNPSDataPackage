import requests
from bs4 import BeautifulSoup

def get_massive_private_dataset_filelist(accession, username, password):
    url = "https://massive.ucsd.edu/ProteoSAFe/dataset_files.jsp?accession={}".format(accession)

    r = requests.get(url, auth=(username, password))

    if r.status_code != 200:
        raise Exception("Unable to get dataset file list")

    r = requests.get(dataset_files_url)
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