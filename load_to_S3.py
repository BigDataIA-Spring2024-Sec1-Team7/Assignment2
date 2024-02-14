
import os
from dotenv import load_dotenv
import boto3

# Load environment variables from .env file
load_dotenv()

# client = boto3.client('s3')

# bucket = 's3'
# cur_path = os.getcwd()
# file = ''

# filename = os.path.join(cur_path, data, file)

# data = open(filename, 'rb')

# client.upload_file(filename, bucket, 'somefile.csv')



def upload_csv_to_s3(csv_file_path, bucket_name, s3_key):
    """
    Uploads a CSV file to an S3 bucket.

    Parameters:
    - csv_file_path (str): The local path to the CSV file to upload.
    - bucket_name (str): The name of the S3 bucket to upload to.
    - s3_key (str): The S3 key to use for the uploaded file.

    Returns:
    - bool: True if the upload was successful, False otherwise.
    """
    try:
        # Initialize S3 client
        s3 = boto3.client('s3', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                          aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                          region_name=os.getenv('AWS_DEFAULT_REGION'))

        # Upload the file
        with open(csv_file_path, 'rb') as f:
            s3.upload_fileobj(f, bucket_name, s3_key)

        print(f"File uploaded successfully to s3://{bucket_name}/{s3_key}")
        return True
    except Exception as e:
        print(f"Error uploading file to S3: {e}")
        return False

# Example usage:
csv_file_path = './cfascraping_data.csv'
bucket_name = 's3-assignment2'
s3_csv = 'cfa_csv/cfascraping_data.csv'
s3_txt1 = 'files_txt/PyPDF_RR_2024_l1_combined.txt'
s3_txt2 = 'files_txt/PyPDF_RR_2024_l2_combined.txt'
s3_txt3 = 'files_txt/PyPDF_RR_2024_l3_combined.txt'
txt_file_path1= './PyPDF_RR_2024_l1_combined.txt'
txt_file_path2= './PyPDF_RR_2024_l2_combined.txt'
txt_file_path3= './PyPDF_RR_2024_l3_combined.txt'

upload_csv_to_s3(csv_file_path, bucket_name, s3_csv)
upload_csv_to_s3(txt_file_path1, bucket_name, s3_txt1)
upload_csv_to_s3(txt_file_path2, bucket_name, s3_txt2)
upload_csv_to_s3(txt_file_path3, bucket_name, s3_txt3)




