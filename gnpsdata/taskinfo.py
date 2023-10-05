import requests
import json

def get_task_information(task, gnps2=True):
    if gnps2:
        url = "https://gnps2.org/status.json?task={}".format(task)

        return requests.get(url).json()
    else:
        url = "https://gnps.ucsd.edu/ProteoSAFe/status_json.jsp?task={}".format(task)
        
        return requests.get(url).json()