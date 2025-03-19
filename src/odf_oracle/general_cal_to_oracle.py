import collections
import oracledb
from odf_toolbox.odfhdr import OdfHeader
from .general_cal_equation_to_oracle import general_cal_equation_to_oracle
from .general_cal_comments_to_oracle import general_cal_comments_to_oracle
from .sytm_to_timestamp import sytm_to_timestamp

def general_cal_to_oracle(odfobj: OdfHeader, user: str, pwd: str, hoststr: str, 
                          infile: str):
    """"
    Load the general cal header metadata from the ODF object into Oracle.

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

    # global i

    # Create a database connection to an Oracle database.
    connection = oracledb.connect(user + '/' + pwd + '@' + hoststr)

    # Create a cursor to the open connection.
    cursor = connection.cursor()

    # Update the NLS_DATE_FORMAT and NLS_TIMESTAMP_FORMAT for the session.
    cursor.execute(
        "ALTER SESSION SET NLS_TERRITORY='AMERICA'"
        " NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS'"
        " NLS_TIMESTAMP_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF'")

    # Check to see if the ODF structure contains an GENERAL_CAL_HEADER.
    if gch is None:

        print('No GENERAL_CAL_HEADER was present to load into Oracle.')

    # Only one GENERAL_CAL_HEADER to process.
    elif type(gch) is collections.OrderedDict:

        # Get the information from the current GENERAL_CAL_HEADER.
        param = gch.get('PARAMETER_NAME')
        caltype = gch.get('CALIBRATION_TYPE')
        cdt = gch.get('CALIBRATION_DATE')
        adt = gch.get('APPLICATION_DATE')
        # ncoef = gch.get('NUMBER_COEFFICIENTS')
        coef = gch.get('COEFFICIENTS')
        caldate = sytm_to_timestamp(cdt, 'datetime')
        appdate = sytm_to_timestamp(adt, 'datetime')
        gch = []
        cursor.prepare(
            "INSERT INTO ODF_GENERAL_CAL (PARAMETER_CODE, CALIBRATION_TYPE, CALIBRATION_DATE, APPLICATION_DATE, "
            "COEFFICIENT_NUMBER, COEFFICIENT_VALUE, ODF_FILENAME) VALUES (:1, :2, :3, :4, :5, :6, :7)")
        if type(coef) is list:
            # Loop through the GENERAL_CAL_HEADER's Coefficients.
            # All calibrations start with intercept; i.e. coefficient 0.
            for j, c in enumerate(coef):
                gch.append((param, caltype, caldate, appdate, j, c, infile))

            # Execute the Insert SQL statement.
            cursor.executemany(None, gch)

        elif type(coef) is str:

            gch.append((param, caltype, caldate, appdate, 0, coef, infile))

            # Execute the Insert SQL statement.
            cursor.executemany(None, gch)

        # Commit the changes to the database.
        connection.commit()

        # Load the General_Cal_Header.Calibration_Equation into Oracle.
        general_cal_equation_to_oracle(gch, user, pwd, hoststr, i, infile)

        # Load the General_Cal_Header.Calibration_Comments into Oracle.
        general_cal_comments_to_oracle(gch, user, pwd, hoststr, 1, infile)

        print('General_Cal_Header successfully loaded into Oracle.')

    # Multiple GENERAL_CAL_HEADERs to process.
    elif type(gch) is list:

        # Loop through the GENERAL_CAL_HEADER.
        for i, p in enumerate(gch):

            # Get the information from the current GENERAL_CAL_HEADER.
            param = p.get('PARAMETER_NAME')
            caltype = p.get('CALIBRATION_TYPE')
            cdt = p.get('CALIBRATION_DATE')
            adt = p.get('APPLICATION_DATE')
            ncoef = p.get('NUMBER_COEFFICIENTS')
            coef = p.get('COEFFICIENTS')
            caldate = sytm_to_timestamp(cdt, 'datetime')
            appdate = sytm_to_timestamp(adt, 'datetime')
            gch = []
            cursor.prepare(
                "INSERT INTO ODF_GENERAL_CAL (PARAMETER_CODE, CALIBRATION_TYPE, CALIBRATION_DATE, APPLICATION_DATE, "
                "COEFFICIENT_NUMBER, COEFFICIENT_VALUE, ODF_FILENAME) VALUES (:1, :2, :3, :4, :5, :6, :7)")
            if ncoef > 1:
                # Loop through the GENERAL_CAL_HEADER's Coefficients.
                # All calibrations start with intercept; i.e. coefficient 0.
                for j, c in enumerate(coef):
                    gch.append((param, caltype, caldate, appdate, j, c, infile))

                # Execute the Insert SQL statement.
                cursor.executemany(None, gch)

            else:

                gch.append((param, caltype, caldate, appdate, 0, coef, infile))

                # Execute the Insert SQL statement.
                cursor.executemany(None, gch)

            # Commit the changes to the database.
            connection.commit()

            # Load the General_Cal_Header.Calibration_Equation into Oracle.
            general_cal_equation_to_oracle(p, user, pwd, hoststr, i, infile);

            # Load the General_Cal_Header.Calibration_Comments into Oracle.
            general_cal_comments_to_oracle(p, user, pwd, hoststr, i, infile);

            print('General_Cal_Header #', i, ' successfully loaded into Oracle.', sep="")

    # Close the cursor and the connection.
    cursor.close()
    connection.close()
