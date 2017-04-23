# Import the modules we need.
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import datetime
from glob import glob
import json
import os
import re
import requests
import string
import sys
import time


# Path to the data directory into which downloaded JSON is saved.
data_path = os.path.join(".", "data", "raw_data", "movie_reviews")
print(data_path)

# Check for whether os.path exists or not, if not create the dicrectory path
if not os.path.exists(data_path):
    print("Creating data directory: {}".format(data_path))
    os.makedirs(data_path)

if os.path.isdir(data_path):
    print(data_path + " is a directory")
else:
    print(data_path + " is NOT a directory - something is wrong :(")


# NYT API Key needs to be set in the environment before running this notebook.
nyt_archive_key = os.getenv('nyt_archive_key')
#print(nyt_archive_key)

if (nyt_archive_key is None) or (nyt_archive_key == ''):
    print("NYT API key is missing - it should be in an environment variable named 'nyt_archive_key'")
	
# General-purpose utility function for saving an object as JSON to the data directory.
def save_to_json(obj, save_file_path):
    print("saving to file: " + save_file_path)

    with open(save_file_path, "wt") as f:
        json.dump(obj, f)
        
# General function for getting JSON, either by downloading or from a cache file.
def resolve_nyt_json(url, cache_file, request_params={}):
    if os.path.isfile(cache_file):
        # Cache file exists, so use that.
        result = {}
        with open(cache_file, 'rt') as f:
            try:
                result = json.load(f)
            except ValueError:
                result = {}
                
        print("resolve_nyt_json(): returning value from cache file: " + cache_file)
        return result

    # It's not in the cache, so download and save it.
    print("resolve_nyt_json(): downloading from NYT API")

    response = requests.get(url, params=request_params)
    print(response.status_code)
        
    # Sleep after a request, to avoid being rate-limited by the NYT servers.
    time.sleep(5)
    
    if 200 == response.status_code:
        save_to_json(response.json(), cache_file)
    else:
        print("resolve_nyt_json(): error downloading from NYT API ({code})".format(code=response.status_code))
        return {}
        
    return response.json()
	
# URL for calls to movies/v7/reviews
def get_movie_reviews_url():
    return "https://api.nytimes.com/svc/movies/v2/reviews/all.json"

# Name of the cache file for calls to reviews/search.
def get_movie_reviews_cache_file_path(offset):
    filename = "movie_reviews_{offset}.json".format(offset=offset)
    print(filename)
    return os.path.join(data_path, filename)

# Name of the cache file for calls to reviews/search.
def get_movie_reviews_params(offset):
    return {'api-key':nyt_archive_key, 
            'offset':offset}

# Convenience routine for getting the result of movie reviews search.
def resolve_movie_reviews(offset):
    return resolve_nyt_json(get_movie_reviews_url(), 
                            get_movie_reviews_cache_file_path(offset), 
                            get_movie_reviews_params(offset))

# set offset to deal with rate limied 
offset = 0
has_more_reviews = True
while has_more_reviews:
    response = resolve_movie_reviews(offset)
    try:
        has_more_reviews = response['has_more']
        offset += 20
    except:
        # Probably got rate-limited. Sleep and try again...
        time.sleep(60)
    
print("Finished")

