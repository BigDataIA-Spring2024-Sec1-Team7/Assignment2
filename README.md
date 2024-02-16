## Problem Statement
Your task is to create two primary datasets from the 224 refresher readings listed on the
CFA Institute’s website and the topic outlines(attached PDF files). These readings are
crucial for finance professionals looking to improve their finance skills. The datasets will
serve as the backbone for an intelligent application designed for these professionals.

## Project Goals

1. Web Scraping and Dataset Creation:
● Utilize web scraping tools such as Beautiful Soup or Scrapy to extract
information from the provided webpage starting with CFA Institute’s
website . You will then use the links to go to the individual 224 pages
(https://www.cfainstitute.org/membership/professional-development/refresher-readings
/time-series-analysis for example).You will focus on extracting the following
details: Introduction, Learning Outcomes, and Summary. Don’t hardcode
the links.. You should scrape the main page and then scrape the individual
pages.
● Structure the extracted data into a CSV file with the schema: {Name of
the topic, Year, Level, Introduction Summary, Learning
Outcomes, Link to the Summary Page, Link to the PDF File}.
https://www.cfainstitute.org/-/media/documents/protected/refresher-reading/2024/level
2/level2a/RR_2024_L2V1R5_time_series_analysis.pdf is a sample link to the pdf file.
● Develop a Python notebook to automate this process.
2. PDF Extraction:
● Use PyPDF2 and Grobid to extract text from the provided PDF files (Topic
outlines).
● Structure the output into text files, following the naming convention:
Grobid_RR_{Year}_{Level}_combined.txt and
PyPDF_RR_{Year}_{Level}_combined.txt.
● Organize these text files into two separate folders named Grobid and
PyPDF, each containing three text files corresponding to the readings.
● Develop a Python notebook for this extraction process.
3. Database Upload:
● Utilize SQLAlchemy to upload the structured data from step 1 into a
Snowflake database.
● Prepare a Python notebook detailing this upload process.
4. Cloud Storage Integration:
● Write a Python function to upload both the structured data (CSV) and the
extracted text files (from both Grobid and PyPDF) into an AWS S3 bucket.
● Utilize SQLAlchemy to upload the structured metadata from step 2
(Grobid) including the link to the uploaded txt file (from S3) the into a
Snowflake database.
● This function should be documented within a Python notebook.

## Data Sources

- 224 Refresher readings listed on the https://www.cfainstitute.org/en/membership/professional-development/refresher-readings#sort=%40refreadingcurriculumyear%20descending
- The topic outlines (3 pdf's)

## Technologies used
Scrapy, Selenium, SQLAlchemy, GROBID, PyPdf, Amazon S3, Snowflake

## Pre-requisites



Before running this project, ensure you have the following prerequisites installed:

- [Python 3](https://www.python.org/downloads/): This project requires Python 3 to be installed. You can download and install Python 3 from the official Python website.

- [Docker](https://www.docker.com/get-started): Docker is used to containerize and manage dependencies for this project. Make sure Docker is installed on your system. You can download and install Docker from the official Docker website.


## How to run application locally

#### Creating Virtual Environment
1. Create a virtual environment using the command `python -m venv <name of virtual env>`. 
2. Install dependencies required to run the project using `pip install -r path/to/requirements.txt`
3. Activate created virtual env by running `source <name of virtual env>/bin/activate`

#### Webscraping
Webscraping uses selenium with scrapy to get the data from website. It opens the base url and fetches the links listed in the readings page using selenium driver and pagination. Multiple spiders are then spawned to open each link and scrape data from them.

##### How to run
1. Selenium chrome driver compatible with your current chrome version can be downloaded from [here](https://chromedriver.chromium.org/downloads). Put the downloaded executable file into `webscraping` folder.
2. Create a virtual environment using the instructions above and activate it
3. Run `cd scripts/webscraping` to switch directory into webscraping folder
4. Run `python -m scrapy crawl cfaspider` to begin scraping data
5. Results are stored in `scripts/webscraping/data` folder as a csv

#### Scraped data upload to Snowflake
Scraped data is uploaded to snowflake using sqlalchemy. First the database, warehouse and tables required are created. The data is loaded from the csv file into a dataframe using pandas. Database connection is established using snowflake-sqlalchemy connectors and the queries are executed. 

##### How to run
1. Create virtual environment and activate it
2. Change directory into `scripts/dataupload` directory and create a .env file to add the credentials required to connect with snowflake. The required fields are the following
a. `SNOWFLAKE_USER`, snowflake username
b. `SNOWFLAKE_PASS`, snowflake password
c. `SNOWFLAKE_ACC_ID`, snowflake account id
More details on how to obtain the above parameters can be found [here](https://docs.snowflake.com/en/user-guide/admin-account-identifier). Please refer to [snowflake documentation](https://docs.snowflake.com/en/developer-guide/python-connector/sqlalchemy) for further reference on setup.
3. Run the code using the command `python snowflake_upload_scraped_data.py`. The data is uploaded from `scripts/webscraping/data/cfascraping_data.csv`.

#### Docker

GROBID is very easy to install and deploy in a Docker container. GROBID is a machine learning library for extracting, parsing and re-structuring raw documents such as PDF into structured XML/TEI encoded documents with a particular focus on technical and scientific publications

##### How to run
1. Pull the image from docker HUB

```sh
docker pull grobid/grobid:0.8.0
```

2. This will create the grobid image and pull in the necessary dependencies.
Here, we are using 0.8.0 version of Grobid.

3. Once done, run the Docker image and map the port to whatever you wish on
your host. We simply map port 8070 of the host to
port 8070 of the Docker :

```sh
docker run --rm --init --ulimit core=0 -p 8070:8070 lfoppiano/grobid:0.8.0
```

4. Verify the deployment by navigating to your server address in
your preferred browser.

```sh
127.0.0.1:8070
```

## References


[PyPdf](https://pypdf2.readthedocs.io/en/3.0.0/): PyPDF2 is a free and open source pure-python PDF library capable of splitting, merging, cropping, and transforming the pages of PDF files. It can also add custom data, viewing options, and passwords to PDF files. PyPDF2 can retrieve text and metadata from PDFs as well.

[Grobid](https://grobid.readthedocs.io/en/latest/Run-Grobid/): GROBID is a machine learning library for extracting, parsing and re-structuring raw documents such as PDF into structured XML/TEI encoded documents with a particular focus on technical and scientific publications.

## Learning Outcomes
- Web scraping: Using tools Scrapy to extract data from websites.
- Data structuring: Organizing extracted data into a CSV file with specific schema.
- Python programming: Developing Python notebooks to automate processes.
- PDF extraction: Using libraries like PyPDF2 and Grobid to extract text from PDFs.
- Database management: Uploading data to a Snowflake database using SQLAlchemy.
- Cloud storage integration: Uploading data to an AWS S3 bucket and linking metadata in Snowflake.

## Team Information and Contribution

| Name | Contribution % | Contribution |
| --- | --- | --- |
Asawari Kadam | 33.33% | PDF Extraction |
Hariharan Sundaram | 33.33%  | Web Scraping and Data Creation |
Rutuja Kute | 33.33%  | Database upload and cloud storage Integration |
