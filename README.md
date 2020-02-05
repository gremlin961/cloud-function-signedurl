Use a cloud function to create a signedURL when a user uploads a file to a GCS bucket.

This example code will create a temporary signedURL users can use to access a file within a GCS bucket. This Cloud Function uses GCP's Secret Manager to access a service account key and create a temporary key file used to generate the signedURL. Ensure the service account used to run the Cloud Function has accessor access to the secret in Secret Manager. The service account used to run the Cloud Function does not need to be same service account used to generate the signedURL.

Make sure the change the "secret_name" variable in the generate-signedurl.py file on line 36 to the name of your secret you create in Secret Manager.

The signedURL will be printed into the Stackdriver logs, but you can also make small modifications to the code and return the url to other functions or applications.
