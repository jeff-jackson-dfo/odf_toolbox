import glob
import os
from icecream import ic
import oracledb

from odf_toolbox.odfhdr import OdfHeader
from odf_toolbox.cruisehdr import CruiseHeader
from odf_toolbox.eventhdr import EventHeader
from odf_toolbox.meteohdr import MeteoHeader
from odf_toolbox.qualityhdr import QualityHeader
from odf_toolbox.instrumenthdr import InstrumentHeader
from odf_toolbox.generalhdr import GeneralCalHeader
from odf_toolbox.polynomialhdr import PolynomialCalHeader
from odf_toolbox.compasshdr import CompassCalHeader
from odf_toolbox.historyhdr import HistoryHeader
from odf_toolbox.recordhdr import RecordHeader
from odf_toolbox.records import DataRecords
from odf_toolbox import odfutils
    
from odf_oracle import cruise_event_to_oracle
from odf_oracle import event_comments_to_oracle
from odf_oracle import meteo_to_oracle
from odf_oracle import meteo_comments_to_oracle
from odf_oracle import instrument_to_oracle
from odf_oracle import quality_to_oracle
from odf_oracle import quality_tests_to_oracle
from odf_oracle import quality_comments_to_oracle
from odf_oracle import history_to_oracle
from odf_oracle import compass_cal_to_oracle
from odf_oracle import polynomial_cal_to_oracle
# from odf_oracle import general_cal_to_oracle
# from odf_oracle import data_to_oracle

def odf_to_oracle(wildcard: str, username: str, userpwd: str, hoststr: str, 
                  mypath: str) -> None:
    """
    Read ODF files and load them into the ODF_ARCHIVE Oracle database.

    Parameters
    ----------
    wildcard: str 
      used to identify specific ODF files in the supplied directory path.
    user: str
      The username for Oracle account.
    pwd: str
      The password for Oracle account.
    hoststr: str
      Oracle database host information.
    mypath: str
      Directory where ODF files to be loaded reside.

    Returns
    -------
    None
    """

    with oracledb.connect(user=username, password=userpwd, dsn=hoststr) as connection:

      print(f'\nAttempting to load the ODF files in the folder << {mypath} >> '\
            'into ODF_ARCHIVE Oracle database')
      
      os.chdir(mypath)

      # Find all ODF files in the current directory using the input wildcard.
      os.listdir(path = mypath)
      filelist = glob.glob(wildcard)

      if len(filelist) == 0:
          print('No files found.')

      # Loop through the list of ODF files.
      for filename in filelist:
      
        print(f'\nWorking on loading ODF file << {filename} >>:')

        odf = OdfHeader()

        # Read the ODF file
        odf.read_odf(filename)

        # Change all null values to empty strings.
        df = odf.null2empty(odf.data.get_data_frame())
        odf.data.set_data_frame(df)

        # # Load the Cruise_Header and Event_Header information into Oracle.
        odf_file = cruise_event_to_oracle(odf, connection, filename)

        # # Load the Event_Header.Event_Comments into Oracle.
        event_comments_to_oracle(odf, connection, odf_file)

        # # Load the Meteo_Header information into Oracle.
        meteo_to_oracle(odf, connection, odf_file)

        # # Load the Meteo_Header.Meteo_Comments into Oracle.
        meteo_comments_to_oracle(odf, connection, odf_file)

        # # Load the Quality_Header information into Oracle.
        quality_to_oracle(odf, connection, odf_file)

        # # Load the Quality_Header.Quality_Tests into Oracle.
        quality_tests_to_oracle(odf, connection, odf_file)

        # # Load the Quality_Header.Quality_Comments into Oracle.
        quality_comments_to_oracle(odf, connection, odf_file)

        # # Load the Instrument_Header information into Oracle.
        instrument_to_oracle(odf, connection, odf_file)

        # # Load the General_Cal_Header information into Oracle.
        # general_cal_to_oracle(odf, connection, odf_file)

        # # Load the Polynomial_Cal_Header information into Oracle.
        polynomial_cal_to_oracle(odf, connection, odf_file)

        # # Load the Compass_Cal_Header information into Oracle.
        compass_cal_to_oracle(odf, connection, odf_file)

        # # Load the History_Header information into Oracle.
        history_to_oracle(odf, connection, odf_file)

        # # Load the Data into Oracle.
        # data_to_oracle(odf, connection, odf_file)

        print(f'\n<< {filename} >> was successfully loaded into Oracle.\n')

def main():
  
  user = 'ODF_Archive'
  pwd = os.environ.get("ODF_ARCHIVE_PASSWORD")
  host = "VSNSBIOXP74.ENT.DFO-MPO.CA"
  port = 1521
  service_name = "PTRAN.ENT.DFO-MPO.CA"
  hoststr = host + ':' + str(port) + '/' + service_name

  # Test Oracle database connection
  # oracledb.init_oracle_client()
  # connection = oracledb.connect(user + '/' + pwd + '@' + hoststr)
  # ic(connection)
  # connection.close()

  odf_to_oracle('*.ODF', connection, r'C:\\DEV\\GitHub\\odf_toolbox\\tests\\LOAD_TO_ORACLE\\')

  # Get credentials for user from cryptographically secure password manager
  # odf_to_oracle('*.ODF', connection, 'C:\\ODF\\')

if __name__ == "__main__":
  main()
    