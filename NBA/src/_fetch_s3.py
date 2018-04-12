import boto3
import inflection
import pandas as pd
from sqlalchemy import create_engine, text

# S3 stuff
BUCKET = "jgoerner-nba"
s3_client = boto3.client("s3")
s3_resource = boto3.resource("s3").Bucket(BUCKET)
s3_folder_mapping = {
    "raw/dumped" : "source"
}

# postgres connection
engine = create_engine("postgres://postgres:postres@postgres_container:5432")

# query template 
query = text('SELECT * FROM pg_catalog.pg_tables WHERE tablename=:table')

def fetch_data():
    """Fetch Data from S3 and put it into the database"""
    print("\n" + "/"*111)
    print("/" + " "*44 + "DOWNLOAD DATA FROM S3" + " "*44 + "/")
    print("/"*111 + "\n\n")

    for folder_key in s3_folder_mapping.keys():

        for obj in s3_resource.objects.filter(Prefix=folder_key):

            obj_path = obj.key
            obj_filename = obj_path.split("/")[-1]
            table_name = inflection.underscore(obj_filename.split(".")[0])

            # ignore directories
            if not obj_filename:
                continue

            # ignore files with leading underscores
            if obj_filename.startswith("_"):
                continue

            # only import CSV
            if not obj_filename.endswith(".csv"):
                continue

            # start log
            print("#"*(len(obj_path)+15))
            print("# Processing {} #".format(obj_path))
            print("#"*(len(obj_path)+15))

            # don't dowload if table is already present in local postgres
            tbl_already_exists = pd.read_sql(query, con=engine, params={'table': table_name}).shape[0]
            if tbl_already_exists:
                print("Table '{}' already exists".format(table_name))
                print("Skipping\n")
                continue

            # download resource form S3
            print("Downloading")
            csv_file = s3_client.get_object(Bucket=BUCKET, Key=obj_path)
            df = pd.read_csv(csv_file["Body"], sep=";")

            # ingesting into postgres
            try:
                df.to_sql(
                    name=table_name,
                    con=engine,
                    schema=s3_folder_mapping[folder_key],
                    index=False,
                )
                print("Ingesting\n")

            except ValueError as e:
                print(e)
                
if __name__ == "__main__":
    fetch_data()