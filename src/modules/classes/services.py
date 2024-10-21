from botocore.exceptions import ClientError

from src.logger import log
from src.modules.classes import repositories
import requests
import boto3

from src.modules.classes.models import ClassData, ProcessedClass

s3_client = boto3.client('s3')
bucket_name = "thesis-classes"


def save_class(class_data: ClassData):
    res = repositories.save_class(class_data)
    return res


def process_audio_file(audio_url: str, class_id: str):
    try:
        s3 = boto3.client('s3')
        audio_key = audio_url.split('/')[-1]

        audio_file = s3.get_object(Bucket=bucket_name, Key=audio_key)
        audio_data = audio_file['Body'].read()

        post_processor_url = 'http://localhost:8000/'
        response = requests.post(post_processor_url, files={'file': ('file', audio_data)})
        res = response.json()
        processed_class = ProcessedClass(
            class_id=class_id,
            audio_text=res[0],
            summary_text=res[1],
            embeddings=res[2]['embedding'],
        )
        processed_class.class_id = class_id

        repositories.save_processed_class(processed_class)

        if response.status_code != 200:
            repositories.failed_processing_class(class_id)
            raise Exception(f"Post processor service failed with status code {response.status_code}")

    except Exception as e:
        repositories.failed_processing_class(class_id)
        log.error(f"Error processing audio file: {str(e)}")


def get_presigned_url(file_name: str, file_type: str) -> str:
    try:
        presigned_url = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': bucket_name,
                'Key': file_name,
                'ContentType': file_type
            },
            ExpiresIn=3600
        )

        return presigned_url

    except ClientError as e:
        raise Exception(f"Failed to generate presigned URL: {str(e)}")


def get_class(class_id: str):
    return repositories.get_full_class_data(class_id)
#
# def get_classses():
#     return repositories.get_classes()
