This is a package to make it easier to access GNPS Data from various web resources. 

1. GNPS Task Data
1. ReDU Repository Data
1. Structure API
1. MassQL Data Conversions
1. Listing Datasets from public Datasets


## Installation

Use the following command

```
pip install git+https://github.com/Wang-Bioinformatics-Lab/GNPSDataPackage.git
```

## Usage

### FBMN

How to get the quantification information

```
from gnpsdata import workflow_fbmn

quant_df = workflow_fbmn.get_quantification_dataframe(task, gnps2=True)
metadata_df = workflow_fbmn.get_metadata_dataframe(task, gnps2=True)
```
