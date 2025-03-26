import os
import pandas as pd
from icecream import ic

# Read in the parameter file
# The parameter file is a spreadsheet that contains the following columns:
# code, description, units, field_width, decimal_places.
# This file contains the parameter definitions used in ODF files.
os.chdir('\\')
drive = os.getcwd()
folder_path = ['DEV', 'ODS_Toolbox', 'ODS1', 'odstools', 'params']
parameter_file = 'gf3defs_sorted.xlsx'
path_to_parameter_file = os.path.join(drive, *folder_path, parameter_file)
data = pd.read_excel(path_to_parameter_file)
data.columns = ['code', 'description', 'units', 'field_width', 'decimal_places']
ic(data)
