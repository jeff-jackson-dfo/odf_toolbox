from odf_oracle.database_connection_pool import get_database_pool

def lookup_parameter(parameter: str) -> dict:
    """ Get the parameter information from the ODF database."""

    # Acquire a connection from the pool (will always have the new date and
    # timestamp formats).
    pool = get_database_pool()
    connection = pool.acquire()

    sql_statement = f"select * from ODF_PARAMETERS where code = '{parameter}'"
    with connection.cursor() as cursor:
        for row in cursor.execute(sql_statement):
            result = row

        column_names = [desc[0].lower() for desc in cursor.description]
        parameter_info = dict(zip(column_names, result))

    # Release the connection back to the pool and close the pool.
    pool.drop(connection)
    pool.close()

    return parameter_info


def main():

    # Get parameter information for TURB from the ODF database.
    parameter = 'TURB'
    lookup_parameter(parameter)


if __name__ == '__main__':
    main()