import boto3
import time
import io

def upload_to_s3(file, bucket_name, key):
    s3 = boto3.client("s3", region_name="us-east-1")
    file_content = file.read()
    s3.upload_fileobj(io.BytesIO(file_content), bucket_name, key)
    time.sleep(2)  # Let S3 sync before Textract
    return f"s3://{bucket_name}/{key}"

def extract_text_from_textract(bucket, key):
    textract = boto3.client("textract", region_name="us-east-1")

    response = textract.start_document_text_detection(
        DocumentLocation={"S3Object": {"Bucket": bucket, "Name": key}}
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

