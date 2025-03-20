import collections

from odf_toolbox.odfhdr import OdfHeader
from odf_oracle import general_cal_equation_to_oracle
from odf_oracle import general_cal_comments_to_oracle
from odf_oracle import sytm_to_timestamp

def general_cal_to_oracle(odfobj: OdfHeader, connection, infile: str):
    """"
    Load the general cal header metadata from the ODF object into Oracle.

    Parameters
    ----------
    odfobj: OdfHeader class object
        An ODF object.
    connection: oracledb connection
        Oracle database connection object.
    infile: str
        ODF file currently being loaded into the database.

    Returns
    -------
    None
    """

    # global i

    # Create a cursor to the open connection.
    with connection.cursor() as cursor:

        # Update the NLS_DATE_FORMAT and NLS_TIMESTAMP_FORMAT for the session.
        # cursor.execute(
        #     "ALTER SESSION SET NLS_TERRITORY='AMERICA'"
        #     " NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS'"
        #     " NLS_TIMESTAMP_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF'")

        # Check to see if the ODF structure contains an GENERAL_CAL_HEADER.
        if odfobj.general_cal_headers is None:

            print('No GENERAL_CAL_HEADER was present to load into Oracle.')

        # Only one GENERAL_CAL_HEADER to process.
        elif type(odfobj.general_cal_headers) is collections.OrderedDict:

            # Get the information from the current GENERAL_CAL_HEADER.
            param = odfobj.general_cal_headers[0].get_parameter_code()
            caltype = odfobj.general_cal_headers[0].get_calibration_type()
            cdt = odfobj.general_cal_headers[0].get_calibration_date()
            adt = odfobj.general_cal_headers[0].get_application_date()
            coeffs = odfobj.general_cal_headers[0].get_coefficients()
            caldate = sytm_to_timestamp(cdt, 'datetime')
            appdate = sytm_to_timestamp(adt, 'datetime')
            gch = []
            cursor.prepare(
                "INSERT INTO ODF_GENERAL_CAL (PARAMETER_CODE, "
                "CALIBRATION_TYPE, CALIBRATION_DATE, APPLICATION_DATE, "
                "COEFFICIENT_NUMBER, COEFFICIENT_VALUE, ODF_FILENAME) "
                "VALUES (:1, :2, :3, :4, :5, :6, :7)")
            if type(coeffs) is list:
                # Loop through the GENERAL_CAL_HEADER's Coefficients.
                # All calibrations start with intercept; i.e. coefficient 0.
                for j, coef in enumerate(coeffs):
                    gch.append((param, caltype, caldate, appdate, j, 
                                coef, infile))

                # Execute the Insert SQL statement.
                cursor.executemany(None, gch)

            elif type(coeffs) is str:

                gch.append((param, caltype, caldate, appdate, 0, 
                            coeffs, infile))

                # Execute the Insert SQL statement.
                cursor.executemany(None, gch)

            # Commit the changes to the database.
            connection.commit()

            # Load the General_Cal_Header.Calibration_Equation into Oracle.
            general_cal_equation_to_oracle(gch, connection, i, infile)

            # Load the General_Cal_Header.Calibration_Comments into Oracle.
            general_cal_comments_to_oracle(gch, connection, 1, infile)

            print('General_Cal_Header successfully loaded into Oracle.')

        # Multiple GENERAL_CAL_HEADERs to process.
        elif type(odfobj.general_cal_headers) is list:

            # Loop through the GENERAL_CAL_HEADER.
            for i, general_cal_header in enumerate(odfobj.general_cal_headers):

                # Get the information from the current GENERAL_CAL_HEADER.
                param = general_cal_header.get_parameter_code()
                caltype = general_cal_header.get_calibration_type()
                cdt = general_cal_header.get_calibration_date()
                adt = general_cal_header.get_application_date()
                ncoeffs = general_cal_header.get_number_coefficients()
                coeffs = general_cal_header.get_coefficients()
                caldate = sytm_to_timestamp(cdt, 'datetime')
                appdate = sytm_to_timestamp(adt, 'datetime')
                gch = []
                cursor.prepare(
                    "INSERT INTO ODF_GENERAL_CAL (PARAMETER_CODE, "
                    "CALIBRATION_TYPE, CALIBRATION_DATE, APPLICATION_DATE, "
                    "COEFFICIENT_NUMBER, COEFFICIENT_VALUE, ODF_FILENAME) "
                    "VALUES (:1, :2, :3, :4, :5, :6, :7)")
                if ncoeffs > 1:
                    # Loop through the GENERAL_CAL_HEADER's Coefficients.
                    # All calibrations start with intercept; i.e. coefficient 0.
                    for j, coeff in enumerate(coeffs):
                        gch.append((param, caltype, caldate, appdate, 
                                    j, coeff, infile))

                    # Execute the Insert SQL statement.
                    cursor.executemany(None, gch)

                else:

                    gch.append((param, caltype, caldate, appdate, 
                                0, coeffs, infile))

                    # Execute the Insert SQL statement.
                    cursor.executemany(None, gch)

                # Commit the changes to the database.
                connection.commit()

                # Load the General_Cal_Header.Calibration_Equation into Oracle.
                general_cal_equation_to_oracle(general_cal_header, connection, 
                                               i, infile)

                # Load the General_Cal_Header.Calibration_Comments into Oracle.
                general_cal_comments_to_oracle(general_cal_header, connection, 
                                               1, infile)

                print(f'General_Cal_Header # {i} successfully" \
                      " loaded into Oracle.')
