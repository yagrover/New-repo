import boto3
import time
import io

def upload_to_s3(file, bucket_name, key, aws_creds):
    s3 = boto3.client(
        "s3",
        region_name="us-east-1",
        aws_access_key_id=aws_creds["aws_access_key_id"],
        aws_secret_access_key=aws_creds["aws_secret_access_key"]
    )

def extract_text_from_textract(bucket, key, aws_creds):
    textract = boto3.client(
        "textract",
        region_name="us-east-1",
        aws_access_key_id=aws_creds["aws_access_key_id"],
        aws_secret_access_key=aws_creds["aws_secret_access_key"]
    )

    job_id = response["JobId"]

    # Wait for job to complete
    while True:
        result = textract.get_document_text_detection(JobId=job_id)
        if result["JobStatus"] in ["SUCCEEDED", "FAILED"]:
            break
        time.sleep(1)

    if result["JobStatus"] != "SUCCEEDED":
        return "❌ Textract failed."

    text = "\n".join([
        block["Text"] for block in result["Blocks"]
        if block["BlockType"] == "LINE"
    ])
    return text

