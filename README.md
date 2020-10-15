# knowlabox-assignment

This repository contains the example code for a Knowlabox API Assignment, using PostgreSQL, ‎Psycopg2, Boto3 with Flask.

## Tasks

- Resize a image to 1000 by 1000 and upload to AWS s3 bucket and also store details in database
- Get image url by file ID


## Setup

1. Clone this repository.
2. Create a virtualenv and activate.
3. Install requirement packages.
4. Open database_credentials.json file and enter all the details for connection with PostgreSQL Database.
5. Open s3_utils.py file and enter Access_key, Secret_key, and bucket name.
6. Start the Flask application on your original terminal window: `flask run`.
7. Go to `http://localhost:5000/`

## Methods


### Resize an Image by URL and store in S3 bucket

```bash
curl -X POST \
  http://localhost:5000/convertimage \
  -H 'Content-Type: application/json' \
  -d "{
	\"img-url\": \"<Image URL>\"
	}"
```
##### Response

```JSON
{   
    "status": "success",
    "message": "Image resize successful",
    "response": "<file-ID>"
}
```


### Retrieving resized image url by file ID

```bash
curl -X POST
http://127.0.0.1:5000/getimagebyfileid \
	-H "Content-Type: application/json"
	-d "{
		\"file_id\":\"<File ID>\",
		}"
```

##### Response

```JSON
{   
    "status": "success",
    "message": "Data Fetched",
    "response": "<Resized Image URL>"
}
```
