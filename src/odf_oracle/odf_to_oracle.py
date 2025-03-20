# import locale
import os
import platform
import oracledb
import glob
from icecream import ic

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
from odf_oracle import general_cal_to_oracle
# from odf_oracle import data_to_oracle

# Set the NLS_DATE_FORMAT for a session
def init_session(connection, requested_tag):
    with connection.cursor() as cursor:
        cursor.execute("alter session set "
        "NLS_LANGUAGE = 'ENGLISH' "
        "NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI' "
        "NLS_TIMESTAMP_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF'")
        

def odf_to_oracle(wildcard: str, user: str, password: str, oracle_host: str,
                  oracle_service_name: str, mypath: str) -> None:
    """
    Read ODF files and load them into the ODF_ARCHIVE Oracle database.

    Parameters
    ----------
    wildcard: str 
      used to identify specific ODF files in the supplied directory path.
    user: str
      The username for Oracle account.
    password: str
      The password for Oracle account.
    oracle_host: str
      Server on which Oracle database exists.
    oracle_service_name: str
      Oracle database service name.
    mypath: str
      Directory where ODF files to be loaded reside.

    Returns
    -------
    None
    """

    # ic(locale.getlocale())
    # locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

    # Change from the default python-oracledb Thin mode to Thick mode.
    oracle_client_dir = None                               # On Linux, no directory should be passed
    if platform.system() == "Darwin":      # macOS
      oracle_client_dir = os.environ.get("HOME")+("/Downloads/instantclient_23_3")
    elif platform.system() == "Windows":   # Windows
      oracle_client_dir = r"C:\Oracle\instantclient_23_7"

    oracledb.init_oracle_client(lib_dir = oracle_client_dir)

    # oracledb.init_oracle_client()

    # connection = oracledb.connect(user = user, 
    #                               password = password, 
    #                               host = oracle_host, 
    #                               port = 1521,
    #                               service_name = oracle_service_name
    #                               )

    pool = oracledb.create_pool(
                                user = user, 
                                password = password, 
                                host = oracle_host, 
                                port = 1521,
                                service_name = oracle_service_name,
                                min = 1, 
                                max = 5, 
                                increment = 1,
                                session_callback = init_session
                                )
    
    # Acquire a connection from the pool (will always have the new date and
    # timestamp formats)
    connection = pool.acquire()
 
    # ic(connection.current_schema)
    # ic(connection.db_name)
    # ic(connection.db_domain)
    # ic(connection.dsn)
    # ic(connection.thin)

    cursor = connection.cursor()

    for row in cursor.execute("select * from NLS_SESSION_PARAMETERS"):
      ic(row)

    cursor.close()

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

    # connection.close()
    pool.drop(connection)
    pool.close()


def main():

  username = "ODF_Archive"
  userpwd = os.environ.get("ODF_ARCHIVE_PASSWORD")
  oracle_host = "VSNSBIOXP74.ENT.DFO-MPO.CA"
  # port = 1521
  oracle_service_name = "PTRAN.ENT.DFO-MPO.CA"
  # hoststr = f"{oracle_host}:{str(port)}/{oracle_service_name}"
  # ic(hoststr)

  # oracledb.init_oracle_client()

  # connection = oracledb.connect(username + '/' + userpwd + '@' + hoststr)
  # cursor = connection.cursor()
  # for row in cursor.execute("select distinct cruise_number from ODF_CRUISE_EVENT where cruise_number like 'HUD2016%'"):
  #   ic(row)
  # cursor.close()
  # connection.close()

  # Test Oracle database connection
  # with oracledb.connect(user = username, 
  #                       password = userpwd, 
  #                       host = oracle_host, 
  #                       port = 1521,
  #                       service_name = oracle_service_name
  #                       ) as connection:    
    # with connection.cursor() as cursor:
    #   for row in cursor.execute("select distinct cruise_number from ODF_CRUISE_EVENT where cruise_number like 'HUD2016%'"):
    #     ic(row)

  odf_to_oracle(wildcard = '*.ODF', 
                user = username, 
                password = userpwd, 
                oracle_host = oracle_host,
                oracle_service_name = oracle_service_name,
                mypath = r'C:\\DEV\\GitHub\\odf_toolbox\\tests\\LOAD_TO_ORACLE\\')


if __name__ == "__main__":
  main()
