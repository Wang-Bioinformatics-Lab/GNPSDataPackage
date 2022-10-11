import networkx
import taskresult

def download_graphml(task, output_file):
    taskresult.download_task_resultfile(task, "gnps_molecular_network_graphml/", output_file)