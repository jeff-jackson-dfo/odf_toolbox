import collections
from icecream import ic

from odf_toolbox.odfhdr import OdfHeader
from odf_oracle.sytm_to_timestamp import sytm_to_timestamp

def compass_cal_to_oracle(odfobj: OdfHeader, connection, infile: str) -> None:
    """"
    Load the compass cal header metadata from the ODF object into Oracle.

    Parameters
    ----------
    odfobj: OdfHeader class object
        An ODF object.
    user: str
        Username of Oracle account.
    pwd: str
        Password for Oracle account.
    hoststr: str
        Oracle database host information.
    infile: str
        ODF file currently being loaded into the database.

    Returns
    -------
    None
    """

    # Create a cursor to the open connection.
    with connection.cursor() as cursor:

        # cursor.execute(
        #     "ALTER SESSION SET "
        #     " NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS'"
        #     " NLS_TIMESTAMP_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF'")

        # print("\nNLS_SESSION_PARAMETERS:")
        # for row in cursor.execute("select * from NLS_SESSION_PARAMETERS"):
        #     ic(row)

        # print("\nNLS_DATABASE_PARAMETERS:")
        # for row in cursor.execute("select * from NLS_DATABASE_PARAMETERS"):
        #     ic(row)

        # Check to see if the ODF object contains an COMPASS_CAL_HEADER.
        if not odfobj.compass_cal_headers:

            print('No COMPASS_CAL_HEADER was present to load into Oracle.')

        # Only one COMPASS_CAL_HEADER to process.
        elif type(odfobj.compass_cal_headers) is collections.OrderedDict:

            compass_cal_header = odfobj.compass_cal_headers[0]

            # Get the information from the current COMPASS_CAL_HEADER.
            param = compass_cal_header.get_parameter_code()
            cdt = compass_cal_header.get_calibration_date()
            adt = compass_cal_header.get_application_date()
            dlist = compass_cal_header.get_directions()
            clist = compass_cal_header.get_corrections()
            cch = []
            caldate = sytm_to_timestamp(cdt, 'datetime')
            appdate = sytm_to_timestamp(adt, 'datetime')
            cursor.prepare(
                "INSERT INTO ODF_COMPASS_CAL (PARAMETER_CODE, CALIBRATION_DATE, "
                "APPLICATION_DATE, DIRECTIONS, CORRECTIONS, ODF_FILENAME) "
                "VALUES (:1, :2, :3, :4, :5, :6)")
            
            if type(dlist) is list:

                # Loop through the COMPASS_CAL_HEADER's DIRECTIONS and Corrections.
                for i, d in enumerate(dlist):
                    cch.append((param, caldate, appdate, d, clist[i], infile))

                # Execute the Insert SQL statement.
                cursor.executemany(None, cch)

            elif type(dlist) is str:

                # Execute the Insert SQL statement.
                cursor.executemany(None, cch)

            # Commit the changes to the database.
            connection.commit()

            print('Compass_Cal_Header successfully loaded into Oracle.')

        # Multiple COMPASS_CAL_HEADER to process.
        elif type(odfobj.compass_cal_headers) is list:

            # Loop through the COMPASS_CAL_HEADER.
            for compass_cal_header in odfobj.compass_cal_headers:

                # Get the information from the current COMPASS_CAL_HEADER.
                param = compass_cal_header.get_parameter_code()
                cdt = compass_cal_header.get_calibration_date()
                adt = compass_cal_header.get_application_date()
                dlist = compass_cal_header.get_directions()
                clist = compass_cal_header.get_corrections()
                caldate = sytm_to_timestamp(cdt, 'datetime')
                appdate = sytm_to_timestamp(adt, 'datetime')
                cch = []
                cursor.prepare(
                    "INSERT INTO ODF_COMPASS_CAL (PARAMETER_CODE, CALIBRATION_DATE, "
                    "APPLICATION_DATE, DIRECTIONS, "
                    "CORRECTIONS, ODF_FILENAME) VALUES (:1, :2, :3, :4, :5, :6)")
                if type(dlist) is list:

                    # Loop through the COMPASS_CAL_HEADER's DIRECTIONS and 
                    # Corrections.
                    for j, dc in enumerate(dlist):
                        cch.append((param, caldate, appdate, dc, clist[j], infile))

                    # Execute the Insert SQL statement.
                    cursor.executemany(None, cch)

                elif type(dlist) is str:

                    # Execute the Insert SQL statement.
                    cursor.executemany(None, cch)

                # Commit the changes to the database.
                connection.commit()

                print('Compass_Cal_Header successfully loaded into Oracle.')

        
        # for row in cursor.execute("SELECT * FROM ODF_COMPASS_CAL WHERE ODF_FILENAME LIKE 'MCM_HUD2010014_1771%' ORDER BY COMPASS_CAL_ID"):
        #     print(row)