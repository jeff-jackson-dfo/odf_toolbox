import oracledb
from odf_toolbox.odfhdr import OdfHeader

def instrument_to_oracle(odfobj: OdfHeader, user: str, pwd: str, hoststr: str, 
                         infile: str) -> None:
    """
    Load the ODF object's instrument header metadata into Oracle.

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

    # Check to see if the ODF structure contains an Instrument_Header.
    if odfobj.instrument_header is None:

        print('No Instrument_Header was present to load into Oracle.')

    else:

        # Create a database connection to an Oracle database.
        connection = oracledb.connect(user + '/' + pwd + '@' + hoststr)

        # Create a cursor to the open connection.
        cursor = connection.cursor()

        # Execute the Insert SQL statement.
        cursor.execute(
            "INSERT INTO ODF_INSTRUMENT (INST_TYPE, INST_MODEL, SERIAL_NUMBER, "
            "DESCRIPTION, ODF_FILENAME) VALUES ("
            ":itype, :imodel, :snum, :description, :fname)",
            {
                'itype': odfobj.instrument_header.get_instrument_type(),
                'imodel': odfobj.instrument_header.get_model(),
                'snum': odfobj.instrument_header.get_serial_number(),
                'description': odfobj.instrument_header.get_description(),
                'fname': infile
            }
        )

        # Commit the changes to the database.
        connection.commit()

        # Close the cursor and the connection.
        cursor.close()
        connection.close()

        print('Instrument_Header successfully loaded into Oracle.')
