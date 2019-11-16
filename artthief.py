#!/usr/bin/env python3

from os.path import expanduser
import os
import random
import json
import requests
import datetime
from pathlib import Path
import argparse

API_URL = "https://api.imgur.com/3"
ALBUMS = []

#TODO: fix paths
def init():
    global BASE_DIR
    BASE_DIR = Path(expanduser("~")) / '.config/artthief'
    if not BASE_DIR.is_dir():
        os.mkdir(BASE_DIR)
    parser = argparse.ArgumentParser(description='Download a random image from a list of imgur album hashes')
    parser.add_argument('--clean', '-c', action='store_true',
                        help='Cleans up old library images before running')
    parser.add_argument('--download-dir', '-d', action='store', dest='downloads',
                        help='Set download directory')
    args = parser.parse_args()

    global DOWNLOAD_DIR
    if args.downloads:
        DOWNLOAD_DIR = Path(args.downloads)
    else:
        DOWNLOAD_DIR = BASE_DIR / 'library'
    if not DOWNLOAD_DIR.is_dir():
        os.mkdir(DOWNLOAD_DIR)
    if args.clean:
        clean()

    config = BASE_DIR / 'albums.conf'
    with open(config, "r") as f:
        for link in f:
            ALBUMS.append(link.rstrip())
    return

def set_base_dir():
    return    

def get_random_album_hash(albums):
    return albums[random.randint( 0, len(ALBUMS)-1 ) ]

def build_album_url_from_hash( album_hash ):
    output = API_URL + '/album/' + album_hash
    return output

def get_json_data_from_response(response):
    return json.loads(response.content)['data']

def get_random_image_from_album_json(json_data):
    count = json_data['images_count']
    r_index = random.randint(0, count-1)
    image = json_data['images'][r_index]
    return image

def download_random_image_from_albums(albums):
    album_hash = get_random_album_hash(albums)
    url = build_album_url_from_hash(album_hash)
    r = requests.get(url, headers={'Authorization': 'Client-ID 8632b98a864f29d'})
    data = get_json_data_from_response(r)
    image = get_random_image_from_album_json(data)
    title = create_file_name(image, album_hash)
    download_image(image['link'], title)

def download_image(url, title):
    path = DOWNLOAD_DIR / title
    r = requests.get(url)
    with open(path, 'wb') as f:  
        f.write(r.content)
    print(path)   

def create_file_name(image_json, album_hash):
    path = str(datetime.date.today()) + '-' + album_hash + '-' + image_json['id']
    title = image_json['title'] 
    if title:
        title = ''.join(e for e in title if e.isalnum())
        path += '-' +title
    path += '.jpg'
    return path

def clean():
    for filename in os.listdir(DOWNLOAD_DIR):
            if filename.endswith(".jpg"):
                os.remove(DOWNLOAD_DIR / filename)

def main():
    init()
    download_random_image_from_albums(ALBUMS)
    
main()
