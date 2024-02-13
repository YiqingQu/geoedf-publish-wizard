# geoedf-publish-wizard
GeoEDF Publish Wizard is an app running on the platform JupyterLab.
## Features
1. Publish file(s) from current Jupyter Lab to persistent storage by calling GeoEDF portal's API.
2. Track the status of previous publishing task.

## Run the app
### Voila
1. `conda activate nbtmpl`
2. `voila notebook.ipynb`. A browser window shoudd open and run the app. If the app doesn't run enter URL "http://localhost:8866/".

### Debugging and Testing
1. `conda activate nbtmpl`
2. `jupyter-lab`
3. Run the notebook `notebook.ipynb` in Jupyter Lab by opening the "Run" menu and selecting "Restart Kernel and Run All Cells..". Then press the the "Restart" button that appears. This will allow you to view any exceptions and errors.
