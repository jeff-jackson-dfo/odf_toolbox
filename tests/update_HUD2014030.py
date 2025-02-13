import glob
import os

# Add path to project 'c:/dev/pythonProjects/odfClass/src/odf_toolbox' to Windows variable PYTHONPATH.
import odfHeader
import odfUtils

cwd = os.getcwd()
path_to_orig = cwd + '/Step_2_Apply_Calibrations/ODF/'
path_to_revised = cwd + '/Step_3_Update_Metadata/'

# Change to folder containing files to be modified
os.chdir(path_to_orig)

# Find all ODF files in the current directory.
files = glob.glob('*.ODF')

# Query the user for his/her name so he/she may be identified in the
# history header as the responsible data quality control person.
# print()
# user = input('Please enter the name of the analyst performing this data processing: ')
user = 'Jeff Jackson'
# print()

# Loop through the list of ODF files and process both the DN and UP files.
# Iterate through the list of input files.
for file_name in files:

    print()
    print('#######################################################################')
    print('Processing ' + file_name)
    print('#######################################################################')
    print()

    odf = odfHeader.OdfHeader()

    # Read the ODF file
    odf.read_odf(file_name)

    # Add a new History Header to record the modifications that are made.
    odf.add_history()
    odf.history_headers[-1].set_creation_date(f"'{odfUtils.get_current_date_time()}'")
    history_comment = f'{user} made the following modifications to this file:'
    odf.add_to_history(history_comment)

    # Update Cruise_Header
    odf.cruise_header.set_organization('DFO BIO')
    odf.cruise_header.set_platform('HUDSON')
    odf.cruise_header.set_start_date('19-SEP-2014 00:00:00.00')
    odf.cruise_header.set_end_date('08-OCT-2014 00:00:00.00')
    odf.cruise_header.set_cruise_name('SCOTIAN SHELF AND SLOPE')
    odf.cruise_header.set_cruise_description('ATLANTIC ZONE MONITORING PROGRAM (AZMP)')

    # Update Event_Header
    odf.event_header.set_set_number('999')
    odf.event_header.set_event_comments('Location Antarctica', 1)

    odf.instrument_header.set_model('SBE 911')

    odf.update_parameter('SYTM_01', 'units', 'GMT')
    odf.update_parameter('SYTM_01', 'print_field_width', 45)

    # Make sure that the event numbers are 3-digit strings.
    odf.event_header.set_event_number('8')
    event_str = odf.event_header.get_event_number()
    event_str = event_str.strip("\' ")
    event_int = int(event_str)
    if len(event_str) < 3:
        odf.event_header.set_event_number(f"{event_int:03}")

    # Add history comments to document that the Slope and Offset values for the primary and secondary conductivity
    # channels were updated from their original acquisition values prior to reprocessing the CTD data files.
    odf.add_to_history(
        'The primary conductivity (3561) and temperature (5081) sensors (pair 1) were replaced with sensors'
        ' (1874) and (2303) (pair 2) after the CTD collided with the bottom prior to event 136.')
    odf.add_to_history('The primary conductivity [3561] calibration coefficient "Offset" was changed from its original '
                       'value [0.0] to [-0.00066] for sensor pair 1.')
    odf.add_to_history('The primary conductivity [3561] calibration coefficient "Slope" was changed from its original '
                       'value [1.0] to [1.000039] for sensor pair 1.')
    odf.add_to_history('The primary conductivity [1874] calibration coefficient "Offset" remained unchanged from its '
                       'original value [0.0] to [0.00048] for sensor pair 2.')
    odf.add_to_history('The primary conductivity [1874] calibration coefficient "Slope" remained unchanged from its '
                       'original value [1.0] to [1.000016] for sensor pair 2.')
    odf.add_to_history('The secondary conductivity [3562] calibration coefficient "Offset" was changed from its '
                       'original value [0.0] to [-0.00132].')
    odf.add_to_history('The secondary conductivity [3562] calibration coefficient "Slope" was changed from its '
                       'original value [1.0] to [1.000272].')

    # Add history comments to document that the Soc values for the primary and secondary oxygen channels were updated
    # from their original acquisition values prior to reprocessing the CTD data files.
    odf.add_to_history('The primary oxygen [0133] calibration coefficient "Soc" was changed from its original value '
                       'of [0.3903] to [0.4054].')
    odf.add_to_history('The secondary oxygen [1588] calibration coefficient "Soc" was changed from its original value '
                       'of [0.5347] to [0.4523].')

    # Access the log records stored in the custom handler and add the logged changes to the History_Header.
    log_records = odfUtils.list_handler.log_records
    for record in log_records:
        odf.add_to_history(record)

    # Update the Record_Header and other headers to revise the metadata after modifications have been performed.
    odf.update_odf()

    odf_file_text = odf.print_object(file_version=2)
    print(odf_file_text)

    os.chdir(path_to_revised)

    # Output a new version of the ODF file using the proper file name.
    out_file = odf.generate_file_spec() + '.ODF'
    print(os.getcwd() + "\\" + out_file)
    file1 = open(out_file, "w")
    file1.write(odf_file_text)
    file1.close()

    os.chdir(path_to_orig)

os.chdir(cwd)

# Run the following script on the MATLAB command line once the
# update_HUD2014030.m script has finished. It creates new files with the
# quality flag fields after running the files through the GTSPP quality
# control checks.
# add_qfs_to_odf('*.ODF', 'C:\DEV\Data\2014\HUD2014030\CTD\DATASHOP_PROCESSING\Step_3_Update_Metadata',
# 'C:\DEV\Data\2014\HUD2014030\CTD\DATASHOP_PROCESSING\Step_4_Run_Automated_Checks', false, false)
