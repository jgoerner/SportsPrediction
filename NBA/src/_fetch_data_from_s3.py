import os
from pathlib import Path
os.chdir("/home/jovyan/work")

import boto3
import pandas as pd

from utils import print_information

@print_information
def fetch_data():
    DATA_DIR = Path("./data")
    
    # get S3 Connection
    s3 = boto3.resource("s3", 
                        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
                       aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"]
                       )
    
    for obj in s3.Bucket("jgoerner-sports-prediction").objects.all():
        # skip file with leading underscore and folder
        name=obj.key
        if name.startswith("_") or name.endswith("/"):
            continue
        print(name)
        
        # check if file already exists
        if Path(DATA_DIR, name).exists():
            print("{} already exists".format(Path(DATA_DIR, name)))
            continue
            
        # check if parent folder exists
        path_segments = name.split("/")
        parent_path = Path(DATA_DIR, *path_segments[:-1])
        if not parent_path.exists():
                parent_path.mkdir(parents=True)
        
        # download the file
        file_path = Path(DATA_DIR, name)
        s3.Bucket("jgoerner-sports-prediction").download_file(name, str(file_path))

if __name__ == "__main__":
    fetch_data()