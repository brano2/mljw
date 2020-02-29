# MLJW

## Setup

* `cd` to the root of the repo
* Install the `htb2020` conda environment by running `conda env create -f environment.yaml`
  * To update the environment later, run `conda env update -f environment.yaml`
* Get your GCP API key JSON file and `export GOOGLE_APPLICATION_CREDENTIALS="/path/to/json"`
  * Alternatively, you can [set up the conda environment](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#macos-and-linux) so that `GOOGLE_APPLICATION_CREDENTIALS` is automatically exported whenever `htb2020` is activated
* [OPTIONAL] set up a PyCharm project for testing the cloud functions
  * Create new Flask project, select `cloud_functions/` as its location, and the `htb2020` conda environment as the interpreter
  * It should complain that the directory is not empty. Choose to create the project from existing sources
* If you prefer to run from terminal instead, `export FLASK_APP=$(readlink -f cloud_functions/app.py)`

## How to run

To run the flask app, either hit the play button in PyCharm, or execute `flask run` in terminal (after `conda activate htb2020`)
