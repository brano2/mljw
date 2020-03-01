# Local cloud function testing

Each file (except `app.py`) corresponds to one cloud function.
The contents can be directly copied to the GCP console. Each file
contains a function named the same as the name of the file. This is
the main function called by google as the cloud function.

The flask app (`app.py`) imports the cloud functions and defines an
endpoint for each of them. This allows for local testing.

If we structure the function files so that the main function only 
handles encoding/decoding of the HTTP/JSON stuff, and helper functions
handle all the actual work, it should be easy to test the functionality
in jupyter notebooks or python scripts as well.
