import os
from dotenv import load_dotenv
from odf_oracle.database_connection_pool import get_database_pool
from odf_oracle.odf_to_oracle import odf_to_oracle

load_dotenv(r'C:/Users/JacksonJ/OneDrive - DFO-MPO/Documents/.env')
username = os.environ.get("ODF_ARCHIVE_USERNAME")
userpwd = os.environ.get("ODF_ARCHIVE_PASSWORD")
oracle_host = os.environ.get("ORACLE_HOST")
oracle_service_name = os.environ.get("ORACLE_SERVICE_NAME")

odf_to_oracle(wildcard = '*.ODF', 
            user = username, 
            password = userpwd, 
            oracle_host = oracle_host,
            oracle_service_name = oracle_service_name,
            mypath = r'C:/DEV/LOAD_TO_ODF_ARCHIVE')
