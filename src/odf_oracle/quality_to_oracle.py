from odf_toolbox.odfhdr import OdfHeader
from odf_oracle import sytm_to_timestamp

def quality_to_oracle(odfobj: OdfHeader, connection, infile: str):
    """
    Load the ODF object's quality header information into Oracle.

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

    # Check to see if the ODF structure contains an QUALITY_HEADER.
    if odfobj.quality_header is None:

        print('No QUALITY_HEADER was present to load into Oracle.')

    else:

        # Create a cursor to the open connection.
        with connection.cursor() as cursor:

            # Execute the Insert SQL statement.
            cursor.execute(
                "INSERT INTO ODF_QUALITY (QUALITY_DATE, ODF_FILENAME) "
                "VALUES (TO_TIMESTAMP(:qdate, 'YYYY-MM-DD "
                "HH24:MI:SS.FF'), :fname)",
                {
                    'qdate': sytm_to_timestamp(
                        odfobj.quality_header.get_quality_date(), 'datetime'),
                    'fname': infile
                }
                )

            # Commit the changes to the database.
            connection.commit()

            print('Quality_Header successfully loaded into Oracle.')
