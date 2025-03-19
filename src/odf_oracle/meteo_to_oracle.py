import oracledb
from odf_toolbox.odfhdr import OdfHeader

def meteo_to_oracle(odfobj: OdfHeader, user: str, pwd: str, hoststr: str, 
                    infile: str) -> None:
    """
    Load the meteo header metadata from the ODF object into Oracle.

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

        print('No METEO_HEADER was present to load into Oracle.')

    else:

        # Create a database connection to the Oracle database.
        connection = oracledb.connect(user + '/' + pwd + '@' + hoststr)

        # Create a cursor to the open database connection.
        cursor = connection.cursor()

        # Execute the Insert SQL statement.
        cursor.execute(
            "INSERT INTO ODF_METEO (AIR_TEMPERATURE, ATMOSPHERIC_PRESSURE, "
            "WIND_SPEED, WIND_DIRECTION, SEA_STATE, "
            "CLOUD_COVER, ICE_THICKNESS, ODF_FILENAME) "
            "VALUES (:at, :ap, :ws, :wd, :ss, :cc, :ice, :fname)",
            {
                'at': odfobj.meteo_header.get_air_temperature(),
                'ap': odfobj.meteo_header.get_atmospheric_pressure(),
                'ws': odfobj.meteo_header.get_wind_speed(),
                'wd': odfobj.meteo_header.get_wind_direction(),
                'ss': odfobj.meteo_header.get_sea_state(),
                'cc': odfobj.meteo_header.get_cloud_cover(),
                'ice': odfobj.meteo_header.get_ice_thickness(),
                'fname': infile
            }
            )

        # Commit the changes to the database.
        connection.commit()

        # Close the cursor and the connection.
        cursor.close()
        connection.close()

        print('Meteo_Header successfully loaded into Oracle.')
