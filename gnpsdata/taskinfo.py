import requests
import json

def get_task_information(task):
    url = "https://gnps.ucsd.edu/ProteoSAFe/status_json.jsp?task={}".format(task)
    return requests.get(url).json()