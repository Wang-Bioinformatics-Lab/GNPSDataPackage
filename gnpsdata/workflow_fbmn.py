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

def download_quantification(task, output_file, gnps2=True):
    if gnps2:
        taskresult.download_gnps2_task_resultfile(task, "nf_output/clustering/featuretable_reformated.csv", output_file)
    else:
        taskresult.download_task_resultfile(task, "quantification_table/", output_file)

def download_metadata(task, output_file, gnps2=True):
    if gnps2:
        taskresult.download_gnps2_task_resultfile(task, "nf_output/metadata/merged_metadata.tsv", output_file)
    else:
        taskresult.download_task_resultfile(task, "metadata_merged/", output_file)

def download_mgf(task, output_file, gnps2=True):
    if gnps2:
        taskresult.download_gnps2_task_resultfile(task, "nf_output/clustering/spectra_reformatted.mgf", output_file)
    else:
        taskresult.download_task_resultfile(task, "spectra_reformatted/", output_file)

# Qiime2 Data
def download_qiime2(task, output_file):
    taskresult.download_task_resultfile(task, "qiime2_output/qiime2_table.qza", output_file)

def download_qiime2_manifest(task, output_file):
    taskresult.download_task_resultfile(task, "qiime2_output/qiime2_manifest.tsv", output_file)

def download_qiime2_metadata(task, output_file):
    taskresult.download_task_resultfile(task, "qiime2_output/qiime2_metadata.tsv", output_file)
