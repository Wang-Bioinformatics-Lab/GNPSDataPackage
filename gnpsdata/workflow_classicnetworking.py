import networkx as nx
from gnpsdata import taskresult

def download_graphml(task, output_file):
    taskresult.download_task_resultfile(task, "gnps_molecular_network_graphml/", output_file)

def get_graphml_network(task):
    taskresult.download_task_resultfile(task, "gnps_molecular_network_graphml/", "temp.graphml")

    G = nx.read_graphml("temp.graphml")

    return G

def download_mgf(task, output_file):
    taskresult.download_task_resultfile(task, "spectra/specs_ms.mgf", output_file)


def get_clustersummary_dataframe(task):
    view_name = "view_all_clusters_withID_beta"

    df = taskresult.get_task_resultview_dataframe(task, view_name)

    return df

def get_clusterinfo_dataframe(task):
    view_name = "view_raw_spectra"

    df = taskresult.get_task_resultview_dataframe(task, view_name)

    return df


def get_librarymatches_dataframe(task):
    view_name = "view_all_annotations_DB"

    df = taskresult.get_task_resultview_dataframe(task, view_name)

    return df