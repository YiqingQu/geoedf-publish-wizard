# config.py - Configuration info, rcampbel@purdue.edu, Oct 2023
from dataclasses import dataclass

TAB_TITLES = ['New Publication', 'My Publications']

# Steps for GeoEDF Publish
SELECT_FILES = 'Step 1: Select Files'
EXTRACT_METADATA = 'Step 2: Enter Required Metadata'
REVIEW_PUBLISH_INFO = 'Step 3: Review Publish Information'
PUBLISH = 'Step 4: Publish'
VIEW_PUBLISH_STATUS = 'Step 5: View Publish Status'


# Welcome tab
TASK_LIST_TITLE = 'My Publication(s)'
TASK_LIST_TEXT = '''<p>
<table>
    <thead>
        <tr>
            <th>Title</th>
            <th>Status</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Publication 1</td>
            <td>Published</td>
        </tr>
        <tr>
            <td>Publication 2</td>
            <td>In Progress</td>
        </tr>
    </tbody>
</table>
</p>'''

# <td><a href="https://geoedf-portal.anvilcloud.rcac.purdue.edu/resource/9bedaf44-5da0-44f1-8ba0-ce58eaa99a23" target="_blank">N/A</a></td>

TRACK_TITLE = 'Track status by task_id'


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
