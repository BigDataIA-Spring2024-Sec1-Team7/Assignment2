import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def create_snowflake_engine(query):
    """
    Creates and returns a SQLAlchemy engine for Snowflake.

    Returns:
    - engine: SQLAlchemy engine object

    """
    SNOWFLAKE_ACCOUNT=os.getenv("SNOWFLAKE_ACCOUNT")
    SNOWFLAKE_USER=os.getenv("SNOWFLAKE_USER")
    SNOWFLAKE_PASSWORD=os.getenv("SNOWFLAKE_PASSWORD")

    try:
        # Create SQLAlchemy engine
        engine = create_engine(f'snowflake://{SNOWFLAKE_USER}:{SNOWFLAKE_PASSWORD}@{SNOWFLAKE_ACCOUNT}/')
        # connection = engine.connect()
        # result = connection.execute(query)
        return engine
    except Exception as e:
        print(f"Error creating Snowflake engine: {e}")
        return None, None

# Example usage:
query = "SELECT current_version()"
engine = create_snowflake_engine(query)


if engine:
    print("Snowflake engine created successfully.")
    print(engine)
else:
    print("Failed to create Snowflake engine.")

# if result:
#     print(result[0])
# else:
#     print("error")
    
connection = engine.connect()
result = connection.execute(query)
print(result[0])




   
        
        



