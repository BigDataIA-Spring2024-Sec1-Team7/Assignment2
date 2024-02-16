# Assignment 2

#### Creating Virtual Environment
1. Create a virtual environment using the command `python -m venv <name of virtual env>`. 
2. Install dependencies required to run the project using `pip install -r path/to/requirements.txt`
3. Activate created virtual env by running `source <name of virtual env>/bin/activate`

#### Webscraping
Webscraping uses selenium with scrapy to get the data from website. It opens the base url and fetches the links listed in the readings page using selenium driver and pagination. Multiple spiders are then spawned to open each link and scrape data from them.

##### How to run
1. Selenium chrome driver compatible with your current chrome version can be downloaded from [here](https://chromedriver.chromium.org/downloads). Put the downloaded executable file into `webscraping` folder.
2. Create a virtual environment using the instructions above and activate it
3. Run `cd webscraping` to switch directory into webscraping folder
4. Run `python -m scrapy crawl cfaspider` to begin scraping data
5. Results are stored in `webscraping/data` folder as a csv

#### Scraped data upload to Snowflake
Scraped data is uploaded to snowflake using sqlalchemy. First the database, warehouse and tables required are created. The data is loaded from the csv file into a dataframe using pandas. Database connection is established using snowflake-sqlalchemy connectors and the queries are executed. 

##### How to run
1. Create virtual environment and activate it
2. Change directory into `sqlupload` directory and create a .env file to add the credentials required to connect with snowflake. The required fields are the following
a. `SNOWFLAKE_USER`, snowflake username
b. `SNOWFLAKE_PASS`, snowflake password
c. `SNOWFLAKE_ACC_ID`, snowflake account id
More details on how to obtain the above parameters can be found [here](https://docs.snowflake.com/en/user-guide/admin-account-identifier). Please refer to [snowflake documentation](https://docs.snowflake.com/en/developer-guide/python-connector/sqlalchemy) for further reference on setup.
3. Run the code using the command `python snowflake_upload.py`. The data is uploaded from `webscraping/data/cfascraping_data.csv`.



