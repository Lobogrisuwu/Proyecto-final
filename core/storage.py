# core/storage.py
from storages.backends.s3boto3 import S3Boto3Storage

class SignedS3Storage(S3Boto3Storage):
    # Fuerza URLs firmadas y que NUNCA use dominio custom
    default_acl = "private"
    file_overwrite = False
    custom_domain = None        # <- importantísimo: sin dominio custom
    querystring_auth = True     # <- importantísimo: firmadas siempre