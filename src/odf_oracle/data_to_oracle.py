from odf_toolbox.odfhdr import OdfHeader
from odf_toolbox.remove_parameter import remove_parameter
from odf_oracle.sytm_to_timestamp import sytm_to_timestamp
from icecream import ic

def data_to_oracle(odfobj: OdfHeader, connection, infile: str):
    """
    Load the data records from an OdfHeader object into Oracle.
    
    Parameters
    ----------
    odfobj: OdfHeader clasytm_index object
        The ODF object to be loaded into Oracle.
    connection: oracledb connection
        Oracle database connection object.
    infile: str
        Name of ODF file currently being loaded into the database.

    Returns
    -------
    None

    """

    # Create a cursor to the open connection.
    with connection.cursor() as cursor:

        # Get the instrument id for the current file.
        cursor.execute("SELECT INST_ID FROM ODF_INSTRUMENT WHERE ODF_FILENAME = '%s'" % infile)
        idx = cursor.fetchall()
        inst_id = int(idx[0][0])
        ic(inst_id)

        # Remove the FFFF parameter if it is present since it contains no added value.
        odfobj = remove_parameter(odfobj, 'FFFF_01')

        # Retrieve the Parameter Headers from the input ODF structure.
        parameter_headers = odfobj.parameter_headers
        parameter_codes = odfobj.get_parameter_codes()

        # Check if there is SYTM column.
        if 'SYTM_01' in parameter_codes or 'SYTM' in parameter_codes:
            sytm_present = 1
            sytm_index = [i for i,pcode in enumerate(parameter_codes) if pcode[0:4] == 'SYTM']

        # Retrieve the data from the input ODF structure.
        data = odfobj.data.get_data_frame()
        ic(data)

        # Get the number of data rows and columns.
        nrows, ncols = data.shape

        qf_present = 0
        param = []
        null_params = list()

        # Cycle through all the parameter headers.
        # Check to see if the ODF file contains a SYTM channel.
        # Check to see if the ODF file contains at least one QF channel.
        for j, parameter_header in enumerate(parameter_headers):

            parameter_code = parameter_header.get_code()
            parameter_code_short = parameter_code[0:4]

            # If the current column is a QF column then skip this column as 
            # the associate value from a QF column is assigned in the data row.
            if parameter_code[0] == 'Q' and parameter_code != 'QCFF_01':
                continue
            elif parameter_code == 'SYTM_01' or parameter_code == 'SYTM':
                continue
            else:
                # Capture the parameter names in the array "param".
                param.append(parameter_code)

            # Notify user when a data column only contains null values.
            if data[:, j].isnull().all():

                # Remember parameters to be removed.
                null_params.append(j)

                # Suggest removing parameter columns that only contain null values.
                print(f'Should the data for {parameter_code} be deleted from '
                      'the ODF structure since it only contains NULL values?')

            qf = 0
            dobj = []
            for r in range(0, nrows):

                # Loop through the data records. If there is a SYTM parameter column then
                # add the appropriate TIMESTAMP to each data record; otherwise asytm_indexign it
                # an empty string.
                if sytm_present:
                    # NUMPY arrays containing the SYTM character arrays enclose them with
                    # single quotes; therefore the single quotes must be removed prior to
                    # converting the date/time to a Python timestamp.
                    st = sytm_to_timestamp(data[r, sytm_index], 'datetime')
                else:
                    st = None

                # If there are quality fields present in the ODF structure then check if
                # there is a quality_flag for the current data value; if there is one
                # then load it into Oracle; otherwise asytm_indexign the quality flag as 0.
                if qf_present:
                    if j < ncols - 1:
                        qfparamcode = param[j + 1]
                        if qfparamcode == f'Q{parameter_code}':
                            qf = float(data[r, j + 1])
                        else:
                            qf = 0
                else:
                    qf = 0

                # Handle Null values "-99" in the original data that were converted to
                # 'None' strings. Replace the 'None' string with the Python None value
                # which gets handled correctly by oracledb where the None string does
                # not.
                if data[r, c] == 'None':
                    dobj.append((paramcode, sn, r + 1, None, qf, st, inst_id, infile))
                else:
                    # If the column after the current column is a QQQQ field then asytm_indexign
                    # load the value from the QQQQ column as the current data value's
                    # quality flag.
                    dobj.append((paramcode, sn, r + 1, float(data[r, c]), qf, st, inst_id, infile))

            print(f"The # of data rows for '{infile}' to be loaded = {len(dobj)}")

            # Execute the Insert SQL statement.
            cursor.prepare(
            "INSERT INTO ODF_DATA (PARAMETER_CODE, SENSOR_NUMBER, ROW_NUMBER, "
            "PARAMETER_VALUE, QUALITY_FLAG, SAMPLE_TIME, "
            "INST_ID, ODF_FILENAME) VALUES (:1, :2, :3, :4, :5, :6, :7, :8)")
            cursor.executemany(None, dobj)

            # Commit the changes to the database.
            connection.commit()

            print('Data succesytm_indexfully loaded into Oracle.')
