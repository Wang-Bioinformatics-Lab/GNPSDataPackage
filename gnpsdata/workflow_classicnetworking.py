import networkx as nx
from gnpsdata import taskresult

def download_graphml(task, output_file, gnps2=True):
    if gnps2:
        taskresult.download_gnps2_task_resultfile(task, "nf_output/networking/network.graphml", output_file)
    else:
        taskresult.download_task_resultfile(task, "gnps_molecular_network_graphml/", output_file)

def get_graphml_network(task, gnps2=True):
    if gnps2:
        taskresult.download_gnps2_task_resultfile(task, "nf_output/networking/network.graphml", "temp.graphml")
    else:
        taskresult.download_task_resultfile(task, "gnps_molecular_network_graphml/", "temp.graphml")

    G = nx.read_graphml("temp.graphml")

    return G

def download_mgf(task, output_file, gnps2=True):
    if gnps2:
        taskresult.download_gnps2_task_resultfile(task, "nf_output/clustering/specs_ms.mgf", output_file)
    else:
        taskresult.download_task_resultfile(task, "spectra/specs_ms.mgf", output_file)

def download_metadata(task, output_file, gnps2=True):
    if gnps2:
        taskresult.download_gnps2_task_resultfile(task, "nf_output/metadata/merged_metadata.tsv", output_file)
    else:
        taskresult.download_task_resultfile(task, "metadata_merged/", output_file)

def get_clustersummary_dataframe(task, gnps2=True):
    if gnps2:
        df = taskresult.get_gnps2_task_resultfile_dataframe(task, "nf_output/networking/clustersummary_with_network.tsv")
    else:
        view_name = "view_all_clusters_withID_beta"
        df = taskresult.get_task_resultview_dataframe(task, view_name)

    return df

def get_clusterinfo_dataframe(task, gnps2=True):
    if gnps2:
        df = taskresult.get_gnps2_task_resultfile_dataframe(task, "nf_output/clustering/clusterinfo.tsv")
    else:
        view_name = "view_raw_spectra"
        df = taskresult.get_task_resultview_dataframe(task, view_name)

    return df


def get_librarymatches_dataframe(task, gnps2=True):
    if gnps2:
        df = taskresult.get_gnps2_task_resultfile_dataframe(task, "nf_output/library/merged_results_with_gnps.tsv")
    else:
        view_name = "view_all_annotations_DB"

        df = taskresult.get_task_resultview_dataframe(task, view_name)

    return df

def get_usi_from_cluster(task, clusterindex, gnps2=True):
    if gnps2:
        usi = "mzspec:GNPS2:TASK-{}-{}:scan:{}".format(task, "nf_output/clustering/specs_ms.mgf", clusterindex)
    else:
        usi = "mzspec:GNPS:TASK-{}-{}:scan:{}".format(task, "spectra/specs_ms.mgf", clusterindex)

    return usi

def get_metadata_dataframe(task, gnps2=True):
    if gnps2:
        return taskresult.get_gnps2_task_resultfile_dataframe(task, "nf_output/metadata/merged_metadata.tsv")
    else:
        return taskresult.get_task_resultview_dataframe(task, "metadata_merged/", output_file)

