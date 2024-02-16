from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from sqlalchemy.engine import URL
import pandas as pd
import numpy as np

load_dotenv()

TABLE_NAME = 'web_scraped_data'
DATABASE_NAME = 'cfa'
WAREHOUSE_NAME = 'cfa_wh'


base_url = URL.create(
    "snowflake",
    username=os.getenv('SNOWFLAKE_USER'),
    password=os.getenv('SNOWFLAKE_PASS'),
    host=os.getenv('SNOWFLAKE_ACC_ID'),
)

# Creating database for storing cfa data
create_cfa_database_query = f"CREATE OR REPLACE DATABASE {DATABASE_NAME};"

# Creating table for scraped data
create_scraped_data_table_query = f"""CREATE OR REPLACE TABLE {TABLE_NAME} (
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
create_cfa_warehouse_query = f"""CREATE OR REPLACE WAREHOUSE {WAREHOUSE_NAME} WITH
    WAREHOUSE_SIZE = 'X-SMALL'
    AUTO_SUSPEND = 180
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE; 
"""

def execute_ddl_queries(connection):
    connection.execute(create_cfa_database_query)
    connection.execute(create_scraped_data_table_query)
    connection.execute(create_cfa_warehouse_query)

def read_and_upload_df(connection):
    connection.execute(f'USE WAREHOUSE {WAREHOUSE_NAME};')
    connection.execute(f'USE DATABASE {DATABASE_NAME};')

    df = pd.read_csv('../webscraping/data/cfascraping_data.csv')
    values_list = []
    for id, row in df.iterrows():
        values_list.append("('{link_summary}', '{topic}', {year}, '{level}', '{link_pdf}', '{intro}', '{learning_outcomes}', '{summary}')".format(
            link_summary=row.link_summary, topic=row.topic, year='NULL' if pd.isnull(row.year) else row.year, level=row.level, link_pdf=row.link_pdf, intro=row.introduction, learning_outcomes=row.learning_outcomes, summary=row.summary
        ))
        # Creating a batch upload of 30 records
        if(len(values_list)%50 == 0):
            values_str = ','.join(values_list)
            execute_insertion(values_str=values_str, id=id)
            values_list = []
    
    if(len(values_list) > 0):
        values_str = ','.join(values_list)
        execute_insertion(values_str=values_str, id=df.size[0])

def execute_insertion(values_str, id):
    try:
        print("Started upload")
        connection.execute("BEGIN")
        connection.execute(f"""INSERT INTO {TABLE_NAME}
                            VALUES
                            {values_str};""")
        connection.execute("COMMIT")
        print(f"Upload successful till record count: {id+1}")
    except Exception as e:
        connection.execute("ROLLBACK")
        print("Exception inserting rows into db. Rolling back! "+str(e))

engine = create_engine(base_url)

try:
    connection = engine.connect()
    execute_ddl_queries(connection=connection)
    read_and_upload_df(connection=connection)
except Exception as e:
    print(e)
finally:
    connection.close()
    engine.dispose()
