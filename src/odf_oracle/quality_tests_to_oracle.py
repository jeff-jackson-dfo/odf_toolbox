import oracledb
from odf_toolbox.odfhdr import OdfHeader

def quality_tests_to_oracle(odfobj: OdfHeader, user: str, pwd: str, 
                            hoststr: str, infile: str):
    """
    Load the ODF object's quality header tests into Oracle.

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

    if odfobj.quality_header is None:

        print('No QUALITY_HEADER Tests were present to load into Oracle.')

    else:

        # Create a database connection to an Oracle database.
        connection = oracledb.connect(user + '/' + pwd + '@' + hoststr)

        # Create a cursor to the open connection.
        cursor = connection.cursor()

        # Loop through the Quality_Header.Quality_Tests.
        quality_tests = odfobj.quality_header.get_quality_tests()
        if type(quality_tests) is list:
            
            for q, quality_test in enumerate(quality_tests):

                # Execute the Insert SQL statement.
                cursor.execute(
                    "INSERT INTO ODF_QUALITY_TESTS (QUALITY_TEST_NUMBER, "
                    "QUALITY_TEST, ODF_FILENAME) VALUES ("
                    ":test_no, :test, :filename)",
                    {
                        'test_no': q,
                        'test': quality_test,
                        'filename': infile
                    }
                    )
                connection.commit()

        elif type(quality_tests) is str:
            
            # Execute the Insert SQL statement.
            cursor.execute(
                "INSERT INTO ODF_QUALITY_TESTS (QUALITY_TEST_NUMBER, "
                "QUALITY_TEST, ODF_FILENAME) VALUES (:test_no, "
                ":test, :filename)",
                {
                    'test_no': 1,
                    'test': quality_tests,
                    'filename': infile
                }
                )
            connection.commit()

        # Close the cursor and the connection.
        cursor.close()
        connection.close()

        print('Quality_Header.Quality_Tests successfully loaded into Oracle.')
