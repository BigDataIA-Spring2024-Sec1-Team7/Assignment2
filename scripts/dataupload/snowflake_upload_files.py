import sqlalchemy
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from sqlalchemy.engine import URL
import pandas as pd
import re

load_dotenv()

DATABASE_NAME = 'cfa'
WAREHOUSE_NAME = 'cfa_wh'

base_url = URL.create(
    "snowflake",
    username=os.getenv('SNOWFLAKE_USER'),
    password=os.getenv('SNOWFLAKE_PASS'),
    host=os.getenv('SNOWFLAKE_ACC_ID'),
)

# Creating database for storing cfa data
create_database_query = f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME};"
create_warehouse_query = f"""CREATE WAREHOUSE IF NOT EXISTS {WAREHOUSE_NAME} WITH
    WAREHOUSE_SIZE = 'X-SMALL'
    AUTO_SUSPEND = 180
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE; 
"""

# Creating table for scraped data
def executeDDLQueries(connection):
    connection.execute(create_database_query)
    connection.execute(create_warehouse_query)
  

engine = create_engine(base_url)

try:
    connection = engine.connect()
    executeDDLQueries(connection=connection)

except Exception as e:
    print(e)
finally:
    connection.close()
    engine.dispose()

def insert_data_to_snowflake(file_path, link, table):
    try:
        # Creating table for scraped data
        base_url = URL.create(
        "snowflake",
        username=os.getenv('SNOWFLAKE_USER'),
        password=os.getenv('SNOWFLAKE_PASS'),
        host=os.getenv('SNOWFLAKE_ACC_ID'),
        )
        engine = create_engine(base_url)
        connection = engine.connect()
        connection.execute(f"USE DATABASE {DATABASE_NAME}")
        connection.execute(f"USE WAREHOUSE {WAREHOUSE_NAME}")
        create_data_table_query = f"""CREATE TABLE IF NOT EXISTS {table} (
            text_column TEXT,
            link_column TEXT
           );
        """
        connection.execute(create_data_table_query)

        # Read the text file
        with open(file_path, 'r') as file:
            text_data = file.read()
            text_data = str(text_data) 
            text_data = re.sub(r'[\'"‘’”“□]|<.*?>', '', text_data).strip('\r\n ')
        link = str(link)
     
        insert_query = f"""INSERT INTO {table} (text_column, link_column) VALUES('''{text_data}''', '{link}');"""

        connection.execute(insert_query)

        print("Data inserted successfully.")
    except Exception as e:
        print("Error:", e)
    finally:
        connection.close()
        engine.dispose()

file_path = '../../notebooks/PyPdf/PyPdf_output/PyPDF_RR_2024_l1_combined.txt'
link = 's3://s3-assignment2/files_txt/PyPDF_RR_2024_l1_combined.txt'
table = 'PyPDF'
insert_data_to_snowflake(file_path, link, table)

file_path = '../../notebooks/PyPdf/PyPdf_output/PyPDF_RR_2024_l2_combined.txt'
link = 's3://s3-assignment2/files_txt/PyPDF_RR_2024_l2_combined.txt'
insert_data_to_snowflake(file_path, link, table)

file_path = '../../notebooks/PyPdf/PyPdf_output/PyPDF_RR_2024_l3_combined.txt'
link = 's3://s3-assignment2/files_txt/PyPDF_RR_2024_l3_combined.txt'
insert_data_to_snowflake(file_path, link, table)


file_path = '../../notebooks/GrobidExtract/Grobid_op/Grobid_RR_2024_l1_combined.txt'
link = 's3://s3-assignment2/files_txt/Grobid_RR_2024_l1_combined.txt'
table = 'GROBID'
insert_data_to_snowflake(file_path, link, table)

file_path = '../../notebooks/GrobidExtract/Grobid_op/Grobid_RR_2024_l2_combined.txt'
link = 's3://s3-assignment2/files_txt/Grobid_RR_2024_l2_combined.txt'
insert_data_to_snowflake(file_path, link, table)

file_path = '../../notebooks/GrobidExtract/Grobid_op/Grobid_RR_2024_l3_combined.txt'
link = 's3://s3-assignment2/files_txt/Grobid_RR_2024_l3_combined.txt'
insert_data_to_snowflake(file_path, link, table)
