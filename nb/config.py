# config.py - Configuration info, rcampbel@purdue.edu, Oct 2023
from dataclasses import dataclass

UPLOAD = 'Step 1: Select Files'
SUBMISSION = 'Step 2: Extract Metadata'
INTEGRITY = 'Step 3: Review the Metadata'
PLAUSIBILITY = 'Step 4: Review Publish Information'
FINISH = 'Publish'
TRACK = 'View Publish Status'

TAB_TITLES = ['Welcome', 'Data']

# Steps for GeoEDF Publish
SELECT_FILES = 'Step 1: Select Files'
EXTRACT_METADATA = 'Step 2: Enter Required Metadata'
REVIEW_PUBLISH_INFO = 'Step 3: Review Publish Information'
PUBLISH = 'Step 4: Publish'
VIEW_PUBLISH_STATUS = 'Step 5: View Publish Status'


# Welcome tab
USING_TITLE = 'Using This App'
USING_TEXT = '''<p>
In the <b>Data</b> tab above, you can review the dataset.
In the <b>Selection</b> tab, you can search for and download data of interest.
Once you've selected data, generate plots in the <b>Visualize</b> tab.
</p>'''
SOURCES_TITLE = 'Data Sources'
SOURCES_TEXT = '''<p>
<b>Land-Ocean Temperature Index</b>
<a href="https://climate.nasa.gov/vital-signs/global-temperature/"
target="_blank">Global Temperature (NASA)</a>
,
<a href="https://data.giss.nasa.gov/gistemp/"
target="_blank">GISS Surface Temperature Analysis (NASA)</a>
</p><p>
This site is based on data downloaded from the following site on 2020-07-14:
<a href="https://data.giss.nasa.gov/gistemp/graphs/graph_data/Global_Mean_Estimates_based_on_Land_and_Ocean_Data/graph.txt"  # noqa
target="_blank">Global Mean Estimates based on Land_and Ocean Data (NASA)</a>
<br>
The code behind this site is intended as a template for anyone wanting to develop similar appliations. Source code
is available <a href="https://github.com/rcpurdue/nbtmpl" target="_blank">here</a>.
</p>'''


MOD = 'Model'  
SCN = 'Scenario'
REG = 'Region'  
VAR = 'Variable'
ITM = 'Item'    
UNI = 'Unit'    
YRS = 'Year'    
VAL = 'Value'   

#       0    1    2    3    4    5    6    7    
HDR = [MOD, SCN, REG, VAR, ITM, UNI, YRS, VAL]

DEL = '-DELETE-RECORDS-'
OVR = '-OVERRIDE-'

NUM_PREVIEW_ROWS = 3
COL_DDN_WIDTH = '140px'

@dataclass
class Project:
    name: str
    group: str
    base: str
    rule_file: str
    submit_dir: str
    pending_dir: str
    merge_file: str


@dataclass
class Config:
    all_projects: list


cfg = Config(
    all_projects=[Project(name='agclim50iv',
                          group='pr-agmipglobaleconagclim50iv',
                          base='/data/projects/agmipglobaleconagclim50iv/files/',
                          rule_file='.rules/RuleTables.xlsx',
                          submit_dir='.submissions/',
                          pending_dir='.submissions/.pending/',
                          merge_file='AgClim50IV.csv'),
                  Project(name='data',
                          group='pr-agmipglobalecondata',
                          base='/data/projects/agmipglobalecondata/files/',
                          rule_file='.rules/RuleTables.xlsx',
                          submit_dir='.submissions/',
                          pending_dir='.submissions/.pending/',
                          merge_file='Data.csv')])
