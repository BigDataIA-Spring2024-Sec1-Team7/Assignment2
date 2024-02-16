from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from sqlalchemy.engine import URL

load_dotenv()

base_url = URL.create(
    "snowflake",
    username=os.getenv('SNOWFLAKE_USER'),
    password=os.getenv('SNOWFLAKE_PASS'),
    host=os.getenv('SNOWFLAKE_ACC_ID'),
)

# Creating database for storing cfa data
create_cfa_database_query = "CREATE OR REPLACE DATABASE cfa;"

# Creating table for scraped data
create_scraped_data_table_query = """CREATE OR REPLACE TABLE web_scraped (
    link_summary STRING,
    topic STRING,
    year INTEGER,
    level STRING,
    link_pdf STRING,
    introduction TEXT,
    learning_outcomes TEXT,
    summary TEXT,
    PRIMARY KEY (link_summary)
)
"""

# Creating warehouse for the cfa databases
create_cfa_warehouse_query = """CREATE OR REPLACE WAREHOUSE cfa_wh WITH
    WAREHOUSE_SIZE = 'X-SMALL'
    AUTO_SUSPEND = 180
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE; 
"""

def executeDDLQueries(connection):
    connection.execute(create_cfa_database_query)
    connection.execute(create_scraped_data_table_query)
    connection.execute(create_cfa_warehouse_query)

engine = create_engine(base_url)

try:
    connection = engine.connect()
    executeDDLQueries(connection=connection)

except Exception as e:
    print(e)
finally:
    connection.close()
    engine.dispose()