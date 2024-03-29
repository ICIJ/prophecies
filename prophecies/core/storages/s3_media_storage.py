from storages.backends.s3boto3 import S3Boto3Storage


# pylint: disable=abstract-method
class S3MediaStorage(S3Boto3Storage):
    location = "private"
    default_acl = "private"
    file_overwrite = False
    custom_domain = False
