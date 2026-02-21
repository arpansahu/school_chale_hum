#!/bin/bash
# Upload static files to MinIO/S3
# Run this script once after setup or when static files change

set -e

echo "==================================="
echo "Uploading Static Files to MinIO"
echo "==================================="

# Load environment variables
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
else
    echo "Error: .env file not found"
    exit 1
fi

# Check if USE_S3 is True
if [ "$USE_S3" != "True" ] && [ "$USE_S3" != "true" ]; then
    echo "Error: USE_S3 is not True. This script is only for S3/MinIO deployments."
    exit 1
fi

echo "Collecting static files locally first..."
python manage.py collectstatic --noinput

echo ""
echo "Static files collected. You can now:"
echo "1. Use mc (MinIO Client) to sync files:"
echo "   mc alias set myminio https://minioapi.arpansahu.space $AWS_ACCESS_KEY_ID $AWS_SECRET_ACCESS_KEY"
echo "   mc cp --recursive staticfiles/ myminio/$AWS_STORAGE_BUCKET_NAME/static/"
echo ""
echo "2. Or use Django storage directly (uncomment below):"
echo ""
# Uncomment if you want automatic upload via Django storage
# python manage.py collectstatic --noinput --clear

echo "✅ Done! Static files are in staticfiles/ directory"
echo "   Upload them to MinIO using mc client or S3 sync tools"
