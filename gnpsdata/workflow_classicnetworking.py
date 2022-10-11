import networkx as nx
from gnpsdata import taskresult

def download_graphml(task, output_file):
    taskresult.download_task_resultfile(task, "gnps_molecular_network_graphml/", output_file)

def get_graphml_network(task):
    #url = taskresult.determine_result_file_url(task, "gnps_molecular_network_graphml/")

    taskresult.download_task_resultfile(task, "gnps_molecular_network_graphml/", "temp.graphml")

    G = nx.read_graphml("temp.graphml")

    print(G)