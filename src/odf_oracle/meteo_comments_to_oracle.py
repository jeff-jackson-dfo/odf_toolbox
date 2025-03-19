import oracledb
from icecream import ic

def meteo_comments_to_oracle(odfobj, user, pwd, hoststr, infile):
    """
    Load the meteo header comments into Oracle.

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

    # Check to see if the ODF object contains an METEO_HEADER.
    if odfobj.meteo_header is None:

        print('No METEO_HEADER Comments to load into Oracle.')

    else:

        # Create a database connection to an Oracle database.
        connection = oracledb.connect(user + '/' + pwd + '@' + hoststr)

        # Create a cursor to the open connection.
        cursor = connection.cursor()

        # Loop through the Meteo_Header.Meteo_Comments.
        meteo_comments = odfobj.meteo_header.get_meteo_comments()

        if type(meteo_comments) is list:

            for j, meteo_comment in enumerate(meteo_comments):
                
                ic(meteo_comment)
            
                # Execute the Insert SQL statement.
                cursor.execute(
                    "INSERT INTO ODF_METEO_COMMENTS (METEO_COMMENT_NUMBER, METEO_COMMENT, ODF_FILENAME) VALUES ("
                    ":comment_no, :comments, :fname)",
                    {
                        'comment_no': j,
                        'comments': meteo_comment,
                        'fname': infile
                    }
                )
                connection.commit()

        elif type(meteo_comments) is str:

            # Execute the Insert SQL statement.
            cursor.execute(
                "INSERT INTO ODF_METEO_COMMENTS (METEO_COMMENT_NUMBER, METEO_COMMENT, ODF_FILENAME) VALUES ("
                ":comment_no, :comments, :fname)",
                {
                    'comment_no': 1,
                    'comments': meteo_comments,
                    'fname': infile
                }
            )
            connection.commit()

        # Close the cursor and the connection.
        cursor.close()
        connection.close()

        print('Meteo_Header.Meteo_Comments successfully loaded into Oracle.')
