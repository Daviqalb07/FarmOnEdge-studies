import os
from pymongo import MongoClient
from gridfs import GridFS


images_db = None


def mongo_conn():
    try:
        conn = MongoClient(host='127.0.0.1', port=27017)
        print("MongoDB connected", conn)
        return conn['images']
    
    except Exception as error:
        print(f"[ERROR] {error}")


def download_image(image_document : dict, download_path : str):
    if not os.path.exists(download_path):
        os.mkdir(download_path)
    
    image_data = get_image_data(image_document)
    image_filename = image_document['filename']

    image_path = download_path + image_filename
    with open(image_path, 'wb') as image:
        image.write(image_data)



def get_image_data(image_document : dict):
    global images_db
    fs = GridFS(images_db)

    id = image_document['_id']
    image_data = fs.get(id).read()
    return image_data


def main():
    global images_db
    images_db = mongo_conn()
    
    images_documents = images_db.fs.files.find()
    download_path = './downloads/'
    for image in images_documents:
        download_image(image, download_path)



main()