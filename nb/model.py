# model.py - Data access, rcampbel@purdue.edu, Oct 2023
import os
import csv
import sys
from fuzzywuzzy import fuzz, process
import pandas as pd
from nb.log import log
from nb.config import HDR, SCN, REG, VAR, ITM, YRS, VAL, NUM_PREVIEW_ROWS, MAP_PUBLICATION_TO_FILE_TYPE

FIX_TBL_SUFFIX = 'FixTable'
FIX_COL = 'Fix'

model = sys.modules[__name__]
model.publication = None

class Publication:
    def __init__(self, publication_type=None, title='', creator='', description='', keywords=''):
        self.publication_type = publication_type
        self.title = title
        self.creator = creator
        self.description = description
        self.keywords = keywords
        self.files = {}
        self.status = 'Draft'

        # Only initialize file structure if a valid publication type is provided
        if publication_type in MAP_PUBLICATION_TO_FILE_TYPE:
            file_types = MAP_PUBLICATION_TO_FILE_TYPE[publication_type]
            for file_type in file_types:
                self.files[file_type] = []

    def set_type(self, publication_type):
        self.files = {}
        if publication_type in MAP_PUBLICATION_TO_FILE_TYPE:
            file_types = MAP_PUBLICATION_TO_FILE_TYPE[publication_type]
            for file_type in file_types:
                self.files[file_type] = []

    def add_file(self, file_path, file_type):
        """
        Adds a file to the publication under the appropriate file type,
        only if the file type is valid for the publication's type.

        :param file_path: Path to the file
        :param file_type: Type of the file, must be valid for the publication's type
        """
        if file_type in self.files:
            self.files[file_type].append({
                'path': file_path,
                'filename': os.path.basename(file_path),
            })

        else:
            print(
                f"File type: {file_type} is not valid for this publication type: {self.publication_type}. File not added.")
        log.debug(f"[CLASS add_file] files: {self.files}")

    def update_metadata(self, publication_type=None, title=None, creator=None, description=None, keywords=None):
        """
        Updates the metadata for the publication.

        :param publication_type: The type of the publication
        :param title: The title of the publication
        :param creator: The creator of the publication
        :param description: The description of the publication
        :param keywords: The keywords associated with the publication
        """
        if publication_type:
            self.publication_type = publication_type
        if title:
            self.title = title
        if creator:
            self.creator = creator
        if description:
            self.description = description
        if keywords:
            self.keywords = keywords

    def publish(self):
        """
        Changes the status of the publication to 'Published'.
        """
        self.status = 'Published'
        # Additional logic to handle the publication process

    def __repr__(self):
        return f"Publication(type={self.publication_type}, title={self.title}, creator={self.creator}, status={self.status})"


# # Example of using the updated Publication class
# pub_workflow = Publication(publication_type=PUBLICATION_TYPE_WORKFLOW,
#                            title='Workflow Publication',
#                            creator='Alice',
#                            description='A detailed workflow publication.',
#                            keywords='workflow, example')
#
# pub_workflow.add_file('/path/to/workflow/process.yml', FILE_TYPE_YAML)
# pub_workflow.add_file('/path/to/data/input.csv', FILE_TYPE_INPUT)
# pub_workflow.add_file('/path/to/results/output.csv', FILE_TYPE_OUTPUT)
#
# # Trying to add a file type that is not valid for the publication type
# pub_workflow.add_file('/path/to/image/map.png', FILE_TYPE_GEOSPATIAL)
#
# print(pub_workflow)
#

def start():
    """Prep model."""
    model.publication = Publication()

def set_file(file_path):
    try:
        model.path = file_path if os.path.getsize(file_path) > 0 else None
    except OSError:
        model.path = None
        raise
        
    return model.path is not None

def detect_delim():
    try:
        with open(model.path, newline='') as f:
            sample = f.read(1024)
            model.detected_delim = csv.Sniffer().sniff(sample).delimiter
    except csv.Error:
        model.detected_delim = None
        raise

    return model.detected_delim is not None

def read_file(delim=None, skip=0, header='infer', ignore=[]):
    try:

        if not header == 'infer':
            header = skip + 0 if header else None

        # TODO use diff dtype for VAL?
        model.df = pd.read_csv(model.path, sep=delim, dtype='category', skiprows=skip, header=header, keep_default_na=False)
        # log.debug(f'read_file(), category mem...\n{model.df.memory_usage(deep=True)}')

    except Exception:
        model.df, model.delim = None, None
        raise

    model.num_rows_read = len(model.df)
    model.ignore_scenarios(ignore)
    return model.df is not None

def ignore_scenarios(ignore, scenario_col=None, remove=False):
    
    if len(ignore) > 0:

        if scenario_col is None:
            # Try to find column holding scenario data
            columns_with_values = model.df.isin(ignore).any(axis=0)
            columns_list = columns_with_values[columns_with_values].index.tolist()
            scenario_col = columns_list[0] if len(columns_list) == 1 else None    

        if scenario_col is not None:
            # Filter using scen col & ignore list 
            filtered_df = model.df[~model.df[scenario_col].isin(ignore)]

            # Save count for integrity tab
            model.num_rows_ignored_scens = len(model.df) - len(filtered_df)

            if remove:
                model.df = filtered_df.reset_index(drop=True)
                model.preview_df = model.df.head(NUM_PREVIEW_ROWS)
            else:
                model.preview_df = filtered_df.copy().reset_index(drop=True).head(NUM_PREVIEW_ROWS) 
    
    else:
        model.num_rows_ignored_scens = 0  # Save count for integrity tab
        model.preview_df = model.df.head(NUM_PREVIEW_ROWS) 

def has_header():
    return isinstance(model.df.columns[0], str)

def load_rules(project):
    """Read all rules from worksheets in project's xlsx file."""
    model.rules = pd.read_excel(os.path.join(project.base, project.rule_file), sheet_name=None, dtype=str, keep_default_na=False)

def all_models():
    return list(model.rules['ModelTable']['Model']) 

def set_columns(col_map):
    """Set column headers, except for model, based on map."""
    hdrs = [''] * len(model.df.columns)

    for i in col_map:
        hdrs[col_map[i]] = HDR[i]

    model.df.columns = hdrs
    log.debug(f'set_columns(), col_map={col_map}, columns={model.df.columns}, df: ...\n{model.df}')

def analyze():
    "Create row counts, bad label list, unknown label list."
    model.num_rows_with_nan = model.df.isna().any(axis=1).sum()  # Row count: Structural problems
    model.duplicate_rows = model.df.duplicated().sum()  # Row count: Duplicate rows
    model.bad_labels, model.unknown_labels = [], []

    # Process output data by column - except values col
    for col in HDR[1:7]:
        data = model.df[col].unique()  # Unique labels in data (+1 to skip model)
        valid = model.rules[col+'Table'][col]  # Valid labels in rules

        # Check each invalid label
        for label in list(set(data) - set(valid)):  
            loc, row, fix, match = None, None, None, None  

            # Is there a fix from a "fix' table in rules?
            if col+FIX_TBL_SUFFIX in model.rules.keys():   
                loc = model.rules[col+FIX_TBL_SUFFIX][col].str.lower() == label.lower()
                row = model.rules[col+FIX_TBL_SUFFIX][loc]
                fix = list(row[FIX_COL])

            # Fix found: add to "bads"
            if (fix is not None) and (len(fix) > 0): 
                model.bad_labels.append((col, label, fix[0]))  
            
            # No fix found: add to "unkowns"
            else:
                match = process.extractOne(str(label), valid.tolist(), scorer=fuzz.token_sort_ratio)  # Closest match
                
                if match is not None and len(match) > 0:
                    model.unknown_labels.append((col, label, match[0]))  # Extract match word from tuple   
                else:
                    model.unknown_labels.append((col, label, None))  

    # Find fixes for value col

    na_mask = pd.to_numeric(model.df[VAL], errors='coerce').isna()     
    non_num_unique = model.df[VAL][na_mask].unique()

    for label in non_num_unique:
        model.bad_labels.append((VAL, label, '0'))  # NOTE Hardcode zero TODO Verify      

def get_valid(col): 
    return sorted(model.rules[col+'Table'][col].tolist())

def get_unique(col):
    return sorted(model.df[col].unique().tolist())

def fix(col, lbl, fix, remove_rows):
    
    if remove_rows:
        model.df = model.df[model.df[col] != lbl]
    else:
        model.df[col] = model.df[col].replace(lbl, fix)

def select(scn, reg, var):
    mask = (model.df[SCN] == scn) & (model.df[REG] == reg) & (model.df[VAR] == var)
    subset = model.df[mask].copy(deep=True)

    # Change year & value cols to numeric
    subset[YRS] = subset[YRS].astype(int) 
    subset[VAL] = subset[VAL].astype(float) 
    
    subset.set_index(YRS, inplace=True)
    return subset.groupby(ITM)[VAL]    

