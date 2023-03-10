import os
import time
from icook.params import *

def load_model():

    from google.cloud import storage
    client = storage.Client()
    blobs = list(client.get_bucket(BUCKET_NAME).list_blobs())
    latest_blob = max(blobs, key=lambda x: x.updated)
    latest_model_path_to_save = os.path.join('icook/model', latest_blob.name)
    latest_blob.download_to_filename(latest_model_path_to_save)

    print(f"✅ Latest model downloaded from cloud storage, to {latest_model_path_to_save}")

    return True
if __name__=='__main__':
    load_model()
