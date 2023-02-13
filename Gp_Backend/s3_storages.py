from storages.backends.s3boto3 import S3Boto3Storage
from Gp_Backend.settings import AWS_S3_BUCKET_NAME


class MediaStorage(S3Boto3Storage):
    bucket_name = AWS_S3_BUCKET_NAME
    custom_domain = f"{bucket_name}.s3.amazonaws.com"
    location = "media"
