import os
from aws_config import get_s3_client

def upload_to_s3(folder_path, bucket_name):
    print("uplaod starts.....")
    s3 = get_s3_client()
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            filepath = os.path.join(folder_path, filename)
            try:
                s3.upload_file(filepath, bucket_name, filename)
                print(f"✅ Uploaded {filename} to s3://{bucket_name}/{filename}")
            except Exception as e:
                print(f"❌ Failed to upload {filename}: {e}")