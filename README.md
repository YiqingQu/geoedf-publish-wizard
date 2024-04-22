# geoedf-publication-wizard
GeoEDF Publish Wizard is a Jupyter Notebook application designed to assist users in preparing and submitting publications. 
This application allows users to select files, extract metadata, review publication information, and submit the publication through the user interface.

## Features
1. Publish to the Portal: 
   1. Select file(s) from current Jupyter Notebook
   2. Extract basic information like user's email, user's `JUPYTERHUB_API_TOKEN` from Jupyter environment variables
   3. Copy file(s) from original directory to staging area
   4. Publish file(s) using the GeoEDF portal's API. 
   5. (The file(s) will be copied to persistent area by the next steps.)
   ![](../../../../var/folders/4z/lvfcfpf5415g5br7f9rb05cm0000gn/T/TemporaryItems/NSIRD_screencaptureui_loivXF/Screen Shot 2024-04-22 at 6.48.57 AM.png)

2. Track Publishing Tasks:
   1. Track the status of your previous publications directly from the interface of the app.
   2. Jump to the resource landing page of a publication in the table
   ![](../../../../var/folders/4z/lvfcfpf5415g5br7f9rb05cm0000gn/T/TemporaryItems/NSIRD_screencaptureui_HyBsu6/Screen Shot 2024-04-22 at 6.49.33 AM.png)
   
## Components
1. `controller.py`: Contains the application logic to handle user interactions and manage the application flow.
2. `view.py`: Manages the user interface components, adjusting the tabs/screens, style and layout
3. `model.py`: Defines the data structure and methods to manage the properties of a publication.
4. `utils.py`: Provides utility functions to interact with external resources and services, like copying directories and sending publication requests through the portal's API.
5. `notebook.ipynb`: The Jupyter Notebook where the application is executed, which initializes and starts the application.


## Run the app
### Debugging and Testing
1. `conda env create --file environment.yml`
2. `conda activate nbtmpl`
3. `jupyter-lab`
4. Run the notebook `notebook.ipynb` in Jupyter Lab by opening the "Run" menu and selecting "Restart Kernel and Run All Cells..". Then press the the "Restart" button that appears. This will allow you to view any exceptions and errors.
5. (If test locally, specify a valid local `base_dir` for `nb/view.py:236`)

### Voila
1. `conda activate nbtmpl`
2. `voila notebook.ipynb`. A browser window shoudd open and run the app. If the app doesn't run enter URL "http://localhost:8866/".


