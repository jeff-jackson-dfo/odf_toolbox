from odf_toolbox.odfhdr import OdfHeader
# import oracledb
from icecream import ic

def event_comments_to_oracle(odfobj: OdfHeader, connection, infile) -> None:
    """
    Load the ODF object's event header comments into Oracle.

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

    # Create a database connection to an Oracle database.
    # connection = oracledb.connect(user + '/' + pwd + '@' + hoststr)

    # Create a cursor to the open connection.
    cursor = connection.cursor()

    # Loop through the Event_Header.Event_Comments.
    event_comments = odfobj.event_header.get_event_comments()
    if type(event_comments) is list:
        for event_comment in event_comments:
            # Execute the Insert SQL statement.
            cursor.execute(
                "INSERT INTO ODF_EVENT_COMMENTS (EVENT_COMMENTS, "
                "ODF_FILENAME) VALUES (:comments, :filename)",
                {
                    'comments': event_comment,
                    'filename': infile
                }
                )
            connection.commit()
    elif type(event_comments) is str:
        # Execute the Insert SQL statement.
        cursor.execute("INSERT INTO ODF_EVENT_COMMENTS (EVENT_COMMENTS, "
        "ODF_FILENAME) VALUES (:comments, :filename)",
                       {
                           'comments': event_comments,
                           'filename': infile
                       }
                       )
        connection.commit()

    # Close the cursor and the connection.
    cursor.close()
    # connection.close()

    print('Event_Header.Event_Comments successfully loaded into Oracle.')
