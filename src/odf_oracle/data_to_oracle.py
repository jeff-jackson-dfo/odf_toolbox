from odf_toolbox import OdfHeader
from odf_toolbox import remove_parameter
from odf_oracle import sytm_to_timestamp
from icecream import ic

def data_to_oracle(odfobj: OdfHeader, connection, infile: str):
    """
    Load the data records from an OdfHeader object into Oracle.
    
    Parameters
    ----------
    odfobj: OdfHeader class object
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

        # Retrieve the Parameter Headers from the input ODF structure.
        param_headers = odfobj.parameter_headers

        # Retrieve the data from the input ODF structure.
        # data1 = odfobj.data.get_data_frame()

        # Remove the FFFF parameter if it is present since it contains no added value.
        odfobj = remove_parameter(odfobj, 'FFFF_01')

        # Retrieve the data from the input ODF structure.
        data = odfobj.get('DATA')

        # Do not include any data columns that only contain null values.
        null_params = list()
        for j, pp in enumerate(param_headers):
            if all(i == data[0, j] for i in data[:, j]):
                # Remember parameters to be removed.
                null_params.append(j)
        if len(null_params) != 0:
            for k in reversed(null_params):
                pp = param_headers[k]
                # Suggest removing parameter columns that only contain null values.
                if pp.get('CODE') is None:
                    print(
                        'Should the data for %s be deleted from the ODF structure since it only contains NULL values?' %
                        pp.get('WMO_CODE'))
                # odfobj = remove_parameter(odfobj, pp.get('WMO_CODE'))
                else:
                    print(
                        'Should the data for %s be deleted from the ODF structure since it only contains NULL values?' %
                        pp.get('CODE'))
                # odfobj = remove_parameter(odfobj, pp.get('CODE'))

        # Retrieve the data from the input ODF structure.
        data = odfobj.get('DATA')

        # Get the number of data rows and columns.
        [nrows, ncols] = data.shape

        # Get the number of parameters.
        # n = len(param_headers)

        # Cycle through all the parameter headers.
        # Check to see if the ODF file contains a PRES channel. If it does then
        # find out which channel it is and if it contains any null values.
        # Check to see if the ODF file contains a SYTM channel.
        # Check to see if the ODF file contains at least one QQQQ channel.
        # pres_present = 0
        sytm_present = 0
        qf_present = 0
        param = []
        pc = []
        ss = -1
        unk = 1
        for i, p in enumerate(param_headers):
            if 'CODE' in p:
                pc = p.get('CODE')
            elif 'WMO_CODE' in p:
                if p.get('WMO_CODE') == 'NONE':
                    pc = "UNKN_%02d" % unk
                    unk = unk + 1
                else:
                    pc = "%s_01" % p.get('WMO_CODE')
            # Capture the parameter names in the array "param".
            param.append(pc)
            # if pc == 'PRES_01' or pc == 'PRES':
            # pres_present = 1
            # pp = i
            if pc == 'SYTM_01' or pc == 'SYTM':
                sytm_present = 1
                ss = i
            if pc == 'QQQQ_01' or pc == 'QQQQ':
                qf_present = 1

        # Because of a bug in Oracle 10.5.0.2 and 11.2.0.1, oracledb 5.1.2; one must
        # change the date and Timestamp formats before inserting data into Oracle.
        cursor.execute(
            "ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS' NLS_TIMESTAMP_FORMAT = 'YYYY-MM-DD HH24:MI:SS.FF'")

        '''
        if sytm_present:    
        print("The # of data rows for '%s' to be loaded = %d" % (infile, nrows * (ncols - 1)))
        else:
        print("The # of data rows for '%s' to be loaded = %d" % (infile, nrows * ncols))
        '''

        # st = ''
        qf = 0
        dobj = []
        for c in range(0, ncols):
            # If the current column is the SYTM parameter then skip this column because
            # these values are being output for each row inserted into Oracle and not
            # as individual data values.
            if c == ss:
                continue
            paramcode = param[c]
            if len(paramcode) >= 6:
                sn = int(paramcode[-2:])
            else:
                sn = None

            # If the current column is either a QQQQ column then skip this column
            # because these values are being output with its associated data value.
            if paramcode[0:4] == 'QQQQ':
                continue
            for r in range(0, nrows):
                # Loop through the data records. If there is a SYTM parameter column then
                # add the appropriate TIMESTAMP to each data record; otherwise assign it
                # an empty string.
                if sytm_present:
                    # NUMPY arrays containing the SYTM character arrays enclose them with
                    # single quotes; therefore the single quotes must be removed prior to
                    # converting the date/time to a Python timestamp.
                    st = sytm_to_timestamp(data[r, ss], 'datetime')
                else:
                    st = None

                # If there are quality fields present in the ODF structure then check if
                # there is a quality_flag for the current data value; if there is one
                # then load it into Oracle; otherwise assign the quality flag as 0.
                if qf_present:
                    if c < ncols - 1:
                        qfparamcode = param[c + 1]
                        if qfparamcode[0:4] == 'QQQQ':
                            qf = float(data[r, c + 1])
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
                    # If the column after the current column is a QQQQ field then assign
                    # load the value from the QQQQ column as the current data value's
                    # quality flag.
                    dobj.append((paramcode, sn, r + 1, float(data[r, c]), qf, st, inst_id, infile))

        print("The # of data rows for '%s' to be loaded = %d" % (infile, len(dobj)))

        # Execute the Insert SQL statement.
        cursor.prepare(
        "INSERT INTO ODF_DATA (PARAMETER_CODE, SENSOR_NUMBER, ROW_NUMBER, PARAMETER_VALUE, QUALITY_FLAG, SAMPLE_TIME, "
        "INST_ID, ODF_FILENAME) VALUES (:1, :2, :3, :4, :5, :6, :7, :8)")
        cursor.executemany(None, dobj)

        # Commit the changes to the database.
        connection.commit()

        print('Data successfully loaded into Oracle.')
