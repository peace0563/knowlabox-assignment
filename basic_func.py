from s3_utils import upload_image_s3_bucket
import requests
import psycopg2
import validators
import json
import uuid
import os
from PIL import Image  

def create_response(status, message="data fetched", response=None):
    response = {
        "status":   status,
        "response": response,
        "message":  message
    }
    return response


def resize_image(img_file_path):
    try:
        ori_img = Image.open(img_file_path)
        newsize = (1000, 1000) 
        resized_img = ori_img.resize(newsize) 
        sav_path = "." + os.path.sep + "temp" + os.path.sep + "resized.jpeg"
        resized_img.save(sav_path, format='JPEG')
        return sav_path
    except Exception as e:
        print(str(e))
        return None


def insert_data_to_db(file_dict):

    # Loading the credentials file that has host URL, username, password of database server
    with open('./database_credentials.json') as p:
        cred = json.load(p)

    # Initiating a connection with database server
    conn = psycopg2.connect(
        "dbname="+cred["dbname"]+" user="+cred["user"]+" host="+cred["host"]+" password="+cred["password"])
    cur = conn.cursor()

    # Insterting values into the table
    cur.execute(
        """INSERT INTO file_table(id, name, url) VALUES (%(file_id)s, %(file_name)s, %(file_url)s)""", file_dict)
    conn.commit()
    cur.close()
    conn.close()


def get_data_from_db(f_id):

    # Loading the credentials file that has host URL, username, password of database server
    with open('./database_credentials.json') as p:
        cred = json.load(p)

    # Initiating a connection with database server
    conn = psycopg2.connect(
        "dbname="+cred["dbname"]+" user="+cred["user"]+" host="+cred["host"]+" password="+cred["password"])
    cur = conn.cursor()

    # Insterting values into the table
    try:
        cur.execute("SELECT * FROM file_table WHERE id = %s", (f_id,))
        data = cur.fetchone()
        return data
    except:
        return None
    finally:
        cur.close()
        conn.close()


def image_url_to_file(url, file_path):
    try:
        response = requests.get(url).content
        with open(file_path, 'wb') as f:
            f.write(response)
        return file_path
    except Exception as e:
        print(str(e))
        return None


def url_validation(inp_url):
    status = validators.url(inp_url)
    if status == True:
        return True
    else:
        return False


def is_image_url(inp_url):
    if inp_url.split(".")[-1] in ["jpeg", "jpg", "gif", "png", "bmp", "tiff"]:
        return True
    return False


def extract_name_from_url(url):
    return url.split("/")[-1]


def conv_image_func(input):
    url = input["img-url"]

    if not url_validation(url):
        response = create_response("error", "Invalid URL")
    elif not is_image_url(url):
        response = create_response("error", "Not an Image URL")
    else:
        file_name = extract_name_from_url(url)
        file_path = "." + os.path.sep + "temp" + \
            os.path.sep + file_name

        file_path = image_url_to_file(url, file_path)
        if file_path == None:
            response = create_response(
                "error", "Couldn't download image, check url and try again.")
        else:
            resize_file_path = resize_image(file_path)
            if resize_file_path == None:
                response = create_response("error", "Couldn't resize image, try again.")
            else:
                status, s3_url_img = upload_image_s3_bucket(
                    resize_file_path, file_name)
                if not status:
                    response = create_response(
                        "error", "Some error occurred, Try again.")
                else:
                    file_dict = {"file_id": str(uuid.uuid4(
                    )), "file_name": file_name, "file_url": s3_url_img}
                    insert_data_to_db(file_dict)
                    response = create_response(
                        "success", "Image resize successful", file_dict["file_id"])
    return response


def get_image_by_id(input):

    f_id = input["file_id"]

    data = get_data_from_db(f_id)

    if data != None:
        response = create_response(
            "success", "data fetched", data[2])
    else:
        response = create_response("error", "no record exists")

    return response
