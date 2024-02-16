import sqlalchemy
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from sqlalchemy.engine import URL
import pandas as pd

load_dotenv()

base_url = URL.create(
    "snowflake",
    username=os.getenv('SNOWFLAKE_USER'),
    password=os.getenv('SNOWFLAKE_PASS'),
    host=os.getenv('SNOWFLAKE_ACC_ID'),
)

# Creating database for storing cfa data
create_database_query = "CREATE OR REPLACE DATABASE all_files;"
create_warehouse_query = """CREATE OR REPLACE WAREHOUSE all_wh WITH
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
# finally:
    # connection.close()
    # engine.dispose()

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
        connection.execute("USE DATABASE all_files")
        connection.execute("USE WAREHOUSE all_wh")
        create_data_table_query = f"""CREATE TABLE IF NOT EXISTS  {table} (
            text_column TEXT,
            link_column TEXT
           );
        """
        connection.execute(create_data_table_query)

        # Read the text file
        with open(file_path, 'r') as file:
            text_data = file.read()
            text_data = str(text_data) 
        link = str(link)
            
      
        
        
     
        insert_query = f"""INSERT INTO {table} (text_column, link_column) VALUES('''{text_data}''', '{link}');"""
        print(insert_query)
    

        connection.execute(insert_query)

        print("Data inserted successfully.")
    except Exception as e:
        print("Error:", e)

# Example usage:
# file_path = './PyPDF_RR_2024_l1_combined.txt'
# link = 's3://s3-assignment2/files_txt/PyPDF_RR_2024_l1_combined.txt'
# table = 'PyPDF'
# insert_data_to_snowflake(file_path, link, table)

# file_path = './PyPDF_RR_2024_l2_combined.txt'
# link = 's3://s3-assignment2/files_txt/PyPDF_RR_2024_l2_combined.txt'
# insert_data_to_snowflake(file_path, link, table)

# file_path = './PyPDF_RR_2024_l3_combined.txt'
# link = 's3://s3-assignment2/files_txt/PyPDF_RR_2024_l3_combined.txt'
# insert_data_to_snowflake(file_path, link, table)


file_path = './Grobid_RR_2024_l1_combined.txt'
link = 's3://s3-assignment2/files_txt/Grobid_RR_2024_l1_combined.txt'
table = 'GROBID'
insert_data_to_snowflake(file_path, link, table)

# file_path = './Grobid_RR_2024_l2_combined.txt'
# link = 's3://s3-assignment2/files_txt/Grobid_RR_2024_l2_combined.txt'
# insert_data_to_snowflake(file_path, link, table)

# file_path = './Grobid_RR_2024_l3_combined.txt'
# link = 's3://s3-assignment2/files_txt/Grobid_RR_2024_l3_combined.txt'
# insert_data_to_snowflake(file_path, link, table)

connection.close()
engine.dispose()


