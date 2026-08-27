"""
Custom storage backends for WIN PROFESSIONAL ACADEMY.
Supports S3-compatible object storage (Cloudflare R2, AWS S3, Backblaze B2, Supabase Storage, MinIO).
"""
import os
from storages.backends.s3 import S3Storage


class PublicMediaStorage(S3Storage):
    """Storage for public media files such as course images, public notes, brochures."""
    location = 'media/public'
    default_acl = None  # Bucket policy or endpoint managed
    file_overwrite = False
    querystring_auth = False


class PrivateMediaStorage(S3Storage):
    """Storage for restricted or protected course materials requiring signed URLs."""
    location = 'media/private'
    default_acl = None
    file_overwrite = False
    querystring_auth = True
    querystring_expire = 3600  # 1 hour signed URL expiration
