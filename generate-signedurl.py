# This file is provided as an example only and is not sutible for use in a production environment
# This script should be used as a GCP Cloud Function and triggered when a data file is uploaded to a GCS
# buicket.

# Import the needed Python modules
from google.cloud import storage
import json
from datetime import datetime, timedelta
# The oauth2client is not currently included in the base Cloud Function python image. Include this module in your requirements.txt file
from oauth2client.client import GoogleCredentials
from google.cloud import secretmanager_v1beta1 as secretmanager
import os, google.auth
from google.auth.transport import requests
from google.auth import compute_engine


# Define a function that will be called by the Cloud Function
def generate_download_signed_url_v4(event, context):
    """Triggered by a change to a Cloud Storage bucket.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    file = event
    # Print the name of the uploaded file that triggered the Cloud Function. The Output will be sent to Stackdriver by default
    print(f"Processing file: {file['name']}.")

    # Properly format the name of the uploaded file, removing any quotation marks left by the json output
    rawname = json.dumps(file['name'])
    rawbucket = json.dumps(file['bucket'])
    filename = rawname.strip('"')
    bucketname = rawbucket.strip('"')
    bucketpath = 'gs://'+bucketname+'/'

    # Generate the signed URL
    client = secretmanager.SecretManagerServiceClient()
    secret_name = "downloader"
    project_id = os.environ["GCP_PROJECT"]
    secret_name = f"projects/{project_id}/secrets/{secret_name}/versions/1"
    response = client.access_secret_version(secret_name)
    secret_string = response.payload.data.decode('UTF-8')
    tmpkey = '/tmp/key.json'
    print('Secret accessed and generating temp key')
    with open(tmpkey, 'w') as outfile:
        outfile.write(secret_string)
    print('temp key file created')

    print('authenticating storage client')
    storage_client = storage.Client.from_service_account_json(tmpkey)
    print('storage client authenticated. Generating download URL')
    bucket = storage_client.bucket(bucketname)
    blob = bucket.blob(filename)
    expires_at_ms = datetime.now() + timedelta(minutes=30)
    url = blob.generate_signed_url(
        # Allows the function to authenticate to the stroage backend
        #credentials=credentials,
        # Denotes the version
        version="v4",
        # This URL is valid for 15 minutes
        expiration=expires_at_ms,
        # Allow GET requests using this URL.
        method="GET"
    )

    print('Download URL is: ' + url)
    #return url
