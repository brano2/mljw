# MLJW

## Setup

* `cd` to the root of the repo
* Install the `htb2020` conda environment by running `conda env create -f environment.yaml`
  * To update the environment later, run `conda env update -f environment.yaml`
* Define environment variables for API keys
  * Get your GCP API key JSON file and `export GOOGLE_APPLICATION_CREDENTIALS="/path/to/json"`
  * Get the NewsAPI key and `export NEWSAPI_KEY="<xxxxxxxxxxxxxxxxxxxxxxxxxxx>"`
  * Alternatively, you can [set up the conda environment](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#macos-and-linux) so that the environment variables are automatically exported whenever `htb2020` is activated
* [OPTIONAL] set up a PyCharm project for testing the cloud functions
  * Create new Flask project, select `cloud_functions/` as its location, and the `htb2020` conda environment as the interpreter
  * It should complain that the directory is not empty. Choose to create the project from existing sources
* If you prefer to run from terminal instead, `export FLASK_APP=$(readlink -f cloud_functions/app.py)`

## How to run

To run the flask app, either hit the play button in PyCharm, or execute `flask run` in terminal (after `conda activate htb2020`)

## Chrome Extension Development

* Install [node](https://nodejs.org/en/). Any version from 8+
* Go to the `ext` directory and run `npm install`. This will install all the necessary dependencies.
* To start developing the extension run `npm run dev`. This will create a `dist` folder.
* To load the extension (`dist` folder) follow the guide on [how to load unpacked extension](https://webkul.com/blog/how-to-install-the-unpacked-extension-in-chrome/)
* To build the extesion run `npm run build`. This will create a zip file ready to be used as an extension.
* Files to edit: `ext/src/contentScripts/index.js` - this file is automatically injected to the site.
* Files to edit: `ext/src/App.vue` - this is the visual of the extension.