from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    """Storage backend for static files with MinIO/S3 support."""
    location = settings.AWS_STATIC_LOCATION
    default_acl = 'public-read'
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    
    # MinIO-specific settings (required for path-style addressing)
    signature_version = 's3v4'
    addressing_style = 'path'
    
    # Set endpoint and credentials based on bucket type
    if hasattr(settings, 'AWS_S3_ENDPOINT_URL'):
        endpoint_url = settings.AWS_S3_ENDPOINT_URL
    if hasattr(settings, 'AWS_ACCESS_KEY_ID'):
        access_key = settings.AWS_ACCESS_KEY_ID
    if hasattr(settings, 'AWS_SECRET_ACCESS_KEY'):
        secret_key = settings.AWS_SECRET_ACCESS_KEY


class PublicMediaStorage(S3Boto3Storage):
    """Storage backend for public media files with MinIO/S3 support."""
    location = settings.AWS_PUBLIC_MEDIA_LOCATION
    default_acl = 'public-read'
    file_overwrite = False
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    
    # MinIO-specific settings
    signature_version = 's3v4'
    addressing_style = 'path'
    
    if hasattr(settings, 'AWS_S3_ENDPOINT_URL'):
        endpoint_url = settings.AWS_S3_ENDPOINT_URL
    if hasattr(settings, 'AWS_ACCESS_KEY_ID'):
        access_key = settings.AWS_ACCESS_KEY_ID
    if hasattr(settings, 'AWS_SECRET_ACCESS_KEY'):
        secret_key = settings.AWS_SECRET_ACCESS_KEY


class ProtectedMediaStorage(S3Boto3Storage):
    """Storage backend for protected media files requiring temporary signed URLs."""
    location = settings.PRIVATE_MEDIA_LOCATION if hasattr(settings, 'PRIVATE_MEDIA_LOCATION') else 'protected'
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False
    querystring_auth = True  # Generate signed URLs
    querystring_expire = 3600  # URLs expire after 1 hour
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    
    # MinIO-specific settings
    signature_version = 's3v4'
    addressing_style = 'path'
    
    if hasattr(settings, 'AWS_S3_ENDPOINT_URL'):
        endpoint_url = settings.AWS_S3_ENDPOINT_URL
    if hasattr(settings, 'AWS_ACCESS_KEY_ID'):
        access_key = settings.AWS_ACCESS_KEY_ID
    if hasattr(settings, 'AWS_SECRET_ACCESS_KEY'):
        secret_key = settings.AWS_SECRET_ACCESS_KEY


class PrivateMediaStorage(S3Boto3Storage):
    """Storage backend for private media files requiring temporary signed URLs."""
    location = 'private'
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False
    querystring_auth = True  # Generate signed URLs
    querystring_expire = 3600  # URLs expire after 1 hour
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    
    # MinIO-specific settings
    signature_version = 's3v4'
    addressing_style = 'path'
    
    if hasattr(settings, 'AWS_S3_ENDPOINT_URL'):
        endpoint_url = settings.AWS_S3_ENDPOINT_URL
    if hasattr(settings, 'AWS_ACCESS_KEY_ID'):
        access_key = settings.AWS_ACCESS_KEY_ID
    if hasattr(settings, 'AWS_SECRET_ACCESS_KEY'):
        secret_key = settings.AWS_SECRET_ACCESS_KEY


