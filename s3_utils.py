import boto3
from botocore.exceptions import ClientError


ACCESS_KEY =  ""
SECRET_KEY = ""
bucket_name = ""

s3_client = boto3.client(
    's3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

location = s3_client.get_bucket_location(Bucket=bucket_name)[
    'LocationConstraint']


def get_s3_obj_url(location, bucket_name, obj_name):
    upload_url = "https://s3-%s.amazonaws.com/%s/%s" % (
        location, bucket_name, obj_name)
    return upload_url


def upload_image_s3_bucket(path, obj_name):
    """
    For force download use this
    meta_data = {'ACL': 'public-read'}

    For view on browser tab use this
    meta_data = {'ACL': 'public-read', 'ContentType': 'image/jpeg'}
    """

    binary_data = None
    meta_data = {'ACL': 'public-read', 'ContentType': 'image/jpeg'}
    try:
        binary_data = open(path, "rb")

        s3_client.upload_fileobj(binary_data, bucket_name,
                                 obj_name, ExtraArgs=meta_data)
        # ExtraArgs={'ACL': 'public-read', 'Metadata': {'recipe_id': '4'}}
        s3_upload_url = get_s3_obj_url(location, bucket_name, obj_name)
        return True, s3_upload_url
    except ClientError as e:
        return False, None
    except Exception as e:
        return False, None
