def general_cal_comments_to_oracle(gch, user, pwd, hoststr, gg, filename):
    """
    ------------------------------------------------------------------------
    CALIBRATION_COMMENTS_TO_ORACLE: Load the GENERAL_CAL_Header comments from the
    input ODF structure into Oracle.

    @author: Jeff Jackson

    @version: 1.0

    @copyright: 2017, Fisheries and Oceans Canada. All Rights Reserved.

    Created: 24-JAN-2017
    Updated: 25-AUG-2022

      Source:
          Ocean Data and Information Services,
          Bedford Institute of Oceanography, DFO, Canada.
          DataServicesDonnees@dfo-mpo.cc.ca

      @summary: Load all the comments from the GENERAL_CAL_Header from the input ODF structure into Oracle.

      Usage:  general_cal_comments_to_oracle(C, user, password, hoststr)

      Input:
            gch: General_Cal portion of an ODF structure array.
           user: Username of Oracle account.
            pwd: Password for Oracle account.
        hoststr: Oracle database host information.
             gg: Iterator identifying the order of the GENERAL_CAL_HEADERS in the ODF file.
       filename: The ODF file name.

      Output:  none

      Example:  general_cal_comments_to_oracle(ODF, 'jj', '1234', 'host:21/dbname', 4, 'filename')

      Updates:

          Jeff Jackson (25-AUG-2022)
          - The Oracle database driver package cx_Oracle was renamed and upgraded to the oracledb package.
          - Reformatted code and made some minor modifications suggested by PyCharm.

    Report any bugs to DataServicesDonnees@dfo-mpo.cc.ca
    ------------------------------------------------------------------------
    """

    import oracledb

    # Create a database connection to an Oracle database.
    connection = oracledb.connect(user + '/' + pwd + '@' + hoststr)

    # Create a cursor to the open connection.
    cursor = connection.cursor()

    # Loop through the General_Cal_Header.General_Cal_Comments.
    cc = gch.get('CALIBRATION_COMMENTS')

    # Check to see if the GENERAL_CAL_HEADER contains any CALIBRATION_COMMENTS.
    if cc is None:

        print('No General_Cal_Header.Calibration_Comments were present to load into Oracle.')

    elif type(cc) is list:
        nc = len(cc)
        for j in range(0, nc):
            # Execute the Insert SQL statement.
            cursor.execute(
                "INSERT INTO ODF_GENERAL_CAL_COMMENTS (GENERAL_CAL_HEADER_NUMBER, CALIBRATION_COMMENT_NUMBER, "
                "CALIBRATION_COMMENT, ODF_FILENAME) VALUES (:cc_no, :comment_no, :comments, :fname)",
                {
                    'cc_no': gg,
                    'comment_no': j,
                    'comments': cc[j],
                    'fname': filename
                }
                )
            connection.commit()
    elif type(cc) is str:
        # Execute the Insert SQL statement.
        cursor.execute(
            "INSERT INTO ODF_GENERAL_CAL_COMMENTS (GENERAL_CAL_HEADER_NUMBER, CALIBRATION_COMMENT_NUMBER, "
            "CALIBRATION_COMMENT, ODF_FILENAME) VALUES (:cc_no, :comment_no, :comments, :fname)",
            {
                'cc_no': gg,
                'comment_no': 1,
                'comments': cc,
                'fname': filename
            }
            )
        connection.commit()

    # Close the cursor and the connection.
    cursor.close()
    connection.close()
