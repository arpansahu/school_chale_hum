#!/usr/bin/env python3
"""Test MinIO/S3 connection and list buckets"""

import os
import sys
from decouple import config
import boto3
from botocore.exceptions import ClientError

# Load settings
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_ENDPOINT_URL = config('AWS_S3_ENDPOINT_URL')

print("=" * 60)
print("Testing MinIO Connection")
print("=" * 60)
print(f"Endpoint: {AWS_S3_ENDPOINT_URL}")
print(f"Bucket: {AWS_STORAGE_BUCKET_NAME}")
print(f"Access Key: {AWS_ACCESS_KEY_ID[:4]}...{AWS_ACCESS_KEY_ID[-4:]}")
print("=" * 60)

try:
    # Create S3 client with MinIO settings
    s3_client = boto3.client(
        's3',
        endpoint_url=AWS_S3_ENDPOINT_URL,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        config=boto3.session.Config(
            signature_version='s3v4',
            s3={'addressing_style': 'path'}
        ),
        verify=True  # SSL verification
    )
    
    print("\n✓ S3 client created successfully")
    
    # Test 1: List buckets
    print("\n[Test 1] Listing all buckets...")
    response = s3_client.list_buckets()
    print(f"✓ Found {len(response['Buckets'])} bucket(s):")
    for bucket in response['Buckets']:
        print(f"  - {bucket['Name']}")
    
    # Test 2: Check if our bucket exists
    print(f"\n[Test 2] Checking if bucket '{AWS_STORAGE_BUCKET_NAME}' exists...")
    try:
        s3_client.head_bucket(Bucket=AWS_STORAGE_BUCKET_NAME)
        print(f"✓ Bucket '{AWS_STORAGE_BUCKET_NAME}' exists and is accessible")
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':
            print(f"✗ Bucket '{AWS_STORAGE_BUCKET_NAME}' does not exist")
        elif error_code == '403':
            print(f"✗ Access denied to bucket '{AWS_STORAGE_BUCKET_NAME}'")
        else:
            print(f"✗ Error: {e}")
        sys.exit(1)
    
    # Test 3: List objects in bucket
    print(f"\n[Test 3] Listing objects in bucket...")
    response = s3_client.list_objects_v2(
        Bucket=AWS_STORAGE_BUCKET_NAME,
        Prefix='static/',
        MaxKeys=10
    )
    
    if 'Contents' in response:
        print(f"✓ Found {response.get('KeyCount', 0)} objects (showing first 10):")
        for obj in response.get('Contents', [])[:10]:
            print(f"  - {obj['Key']} ({obj['Size']} bytes)")
    else:
        print("✓ Bucket is empty or no objects with 'static/' prefix")
    
    # Test 4: Test upload
    print(f"\n[Test 4] Testing upload capability...")
    test_key = 'static/test-connection.txt'
    test_content = 'MinIO connection test successful!'
    
    s3_client.put_object(
        Bucket=AWS_STORAGE_BUCKET_NAME,
        Key=test_key,
        Body=test_content.encode('utf-8'),
        ContentType='text/plain'
    )
    print(f"✓ Successfully uploaded test file: {test_key}")
    
    # Test 5: Test read
    print(f"\n[Test 5] Testing read capability...")
    response = s3_client.get_object(
        Bucket=AWS_STORAGE_BUCKET_NAME,
        Key=test_key
    )
    content = response['Body'].read().decode('utf-8')
    print(f"✓ Successfully read test file: {content}")
    
    # Cleanup
    s3_client.delete_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=test_key)
    print(f"✓ Cleaned up test file")
    
    print("\n" + "=" * 60)
    print("✅ All tests passed! MinIO connection is working.")
    print("=" * 60)
    print("\nYou can now run:")
    print("  python manage.py collectstatic --noinput")
    print("\nTo upload all static files to MinIO.")
    
except ClientError as e:
    print("\n" + "=" * 60)
    print(f"❌ Error: {e}")
    print("=" * 60)
    error_code = e.response.get('Error', {}).get('Code', 'Unknown')
    error_msg = e.response.get('Error', {}).get('Message', str(e))
    print(f"\nError Code: {error_code}")
    print(f"Error Message: {error_msg}")
    
    if error_code == '400' or 'Bad Request' in str(e):
        print("\n🔍 Troubleshooting 400 Bad Request:")
        print("1. Check endpoint URL format (should be https://minioapi.arpansahu.space)")
        print("2. Verify credentials are correct")
        print("3. Ensure bucket name doesn't contain invalid characters")
        print("4. Check if endpoint is reachable:")
        print(f"   curl -I {AWS_S3_ENDPOINT_URL}")
    
    sys.exit(1)
    
except Exception as e:
    print(f"\n❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
