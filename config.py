import os

# Google Cloud Project ID.
PROJECT_ID = os.environ.get('PROJECT_ID')

# CloudSQL & SQLAlchemy configuration
CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')
CLOUDSQL_DATABASE = os.environ.get('CLOUDSQL_DATABASE')
# Set this value to the Cloud SQL connection name, e.g.
#   "project:region:cloudsql-instance".
CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')

# The CloudSQL proxy is used locally to connect to the cloudsql instance.
# To start the proxy, use:
#
#   $ ./cloud_sql_proxy -instances=your-connection-name=tcp:3306
#
# Port 3306 is the standard MySQL port. If you need to use a different port,
# change the 3306 to a different port number.

LIVE_DATABASE_URI = (
        'mysql+pymysql://{user}:{password}@localhost:3307/{database}?charset=utf8').format(
        user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
        database=CLOUDSQL_DATABASE, connection_name=CLOUDSQL_CONNECTION_NAME)

DATABASE_URI = LIVE_DATABASE_URI
