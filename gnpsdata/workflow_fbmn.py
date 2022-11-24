import networkx as nx
from gnpsdata import taskresult

def download_graphml(task, output_file):
    taskresult.download_task_resultfile(task, "gnps_molecular_network_graphml/", output_file)

def get_graphml_network(task):
    taskresult.download_task_resultfile(task, "gnps_molecular_network_graphml/", "temp.graphml")

    G = nx.read_graphml("temp.graphml")

    return G

def download_mgf(task, output_file):
    taskresult.download_task_resultfile(task, "spectra_reformatted/", output_file)
