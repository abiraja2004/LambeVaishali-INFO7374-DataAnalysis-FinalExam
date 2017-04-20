Final submission : Name- Vaishali Lambe : NUID-001286444
=============================================================================================================================
-----------
Synopsis
------------
I have chosen second pattern which downloads data from from NYTimes developer portal (movie reviews API), stores it and performs 3 analysis.
```final``` folder contains the the following files for final exam submission

> - Data collection and storage script location
>```final/data_collectionandstorage_moviereviews.ipynb and final/data_collectionandstorage_moviereviews.py```  file to collect data and store it in a proper directory(folder) structure from NYTimes developer portal of  movie reviews API 

> - Data storage location
>  ```final/data/raw_data/movie_reviews``` This is data storage location

> - Data analysis location
>  ```final/analysis/ana[1-3]``` *.ipynb*  and *.py* files for analysis 1, 2 and 3 

> - Analysis 1 script file location
>  ```final/analysis1.ipynb and final/analysis1.py``` script for analysis 1

> - Analysis 2 script file location
>  ```final/analysis2.ipynb and final/analysis2.py``` script for analysis 2

> - Analysis 3 script file location
>  ```final/analysis3.ipynb and final/analysis3.py``` script for analysis 3

> - Output files
>  ```final/output``` contains all the outputs in *.png* format and .csv format for analysis 1, analysis 2 and analysis 3

-----------
Collecting and Storing Data
------------
> - Wrote *.ipynb* files to gather movie reviews data and store it in mentioned directory location.*os.path.join" is used to give a data path to save downloaded JSON files.
> - ```final/data_collectionandstorage_moviereviews.ipynb and final/data_collectionandstorage_moviereviews.py``` file is used to hit **moviereviews** api of *New York Times*.  
> - If directory path is not present creates directory path

**Logic:**
<*data_collectionandstorage_moviereviews.ipynb/data_collectionandstorage_moviereviews.py*>
> - Exported the nytimes developer api key to bash terminal and read as an *environment variable*
> - I have used **moviereviews** api to fetch data in json format
> - Defined function '''save_to_json''' for saving an object as JSON to the data directory
> - Defined function '''resolve_nyt_json''' for getting JSON, either by downloading or from a cache file. It contains check condition to avoid being rate-limited by the NYT servers and sleep after a request
> - Defined function '''get_movie_reviews_url''' which returns movie reviews url
> - Defined function '''get_movie_reviews_cache_file_path''' which returns path to store it
> - Defined function '''get_movie_reviews_params''' which returns api and offset
> - Defined functon '''resolve_movie_reviews''' for getting the result of movie reviews search
> - Provided check conditin again to check if movie has more reviews so avoid the rate limied and sleep again to download it completely.


 