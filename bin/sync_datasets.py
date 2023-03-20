import sys
import os
import argparse
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from gnpsdata import publicdata

def main():
    # Creating the arguments
    parser = argparse.ArgumentParser(description='Syncing datasets')
    parser.add_argument('dataset_accession', help='Dataset to sync')
    parser.add_argument('output_folder', help='Output folder')

    # Parsing the arguments
    args = parser.parse_args()

    dataset_accession = args.dataset_accession

    print("Downloading {}".format(dataset_accession))

    # Getting public dataset file list
    public_dataset_file_list = publicdata.get_massive_public_dataset_filelist(dataset_accession)

    print(public_dataset_file_list)

    # Doing the actual download
    target_location = os.path.normpath(args.output_folder)
    log_file = "logs.txt"
    
    for file_obj in public_dataset_file_list:
        target_file_folder = os.path.normpath(os.path.join(target_location, file_obj["relative_path"]))
        target_file = os.path.normpath(os.path.join(target_file_folder, file_obj["name"]))

        if os.path.exists(target_file):
            continue

        # Checking if is subdir
        assert(Path(target_location) in Path(target_file_folder).parents)
        assert(Path(target_location) in Path(target_file).parents)

        # Making sure folder exists
        os.makedirs(target_file_folder, exist_ok=True)

        # Downloading file
        url = "https://massive.ucsd.edu/ProteoSAFe/DownloadResultFile?file=f.{}/{}/{}&forceDownload=true".format(dataset_accession, file_obj["relative_path"], file_obj["name"])

        wget_cmd = "wget --no-clobber --no-host-directories --output-document '{}' '{}' >> {} 2>&1".format(target_file, url, log_file)
        
        print(wget_cmd)
        os.system(wget_cmd)
    



if __name__ == "__main__":
    main()