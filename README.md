Final submission : Name- Vaishali Lambe : NUID-001286444
=============================================================================================================================
-----------
Synopsis
------------
I have chosen second pattern which downloads data from from NYTimes developer portal (movie reviews API), stores it and performs 3 analysis.
```final``` folder contains the the following files for final exam submission

-----------
Folder structure and locations for each file 
------------
> - Data collection and storage script location
>```final/data_collection_storage_moviereviews.ipynb and final/data_collection_storage_moviereviews.py```  file to collect data and store it in a proper directory(folder) structure from NYTimes developer portal of  movie reviews API 

> - Raw data storage location
>  ```final/data/raw_data/movie_reviews``` contains all JSON files for movie_reviews

> - Cleaned data storage location
>  ```final/data/cleaned_data``` contains cleaned data in **movie_reviews.csv** file format which is ready for analysis

> - Data analysis location
>  ```final/analysis``` *.ipynb*  and *.py* files for analysis 1, 2 and 3 as ana_1, ana_2, ana_3 

> - Data collection and storage script file location
>  ```final/data_collection_storage_moviereviews.ipynb and final/data_collection_storage_moviereviews.py``` script for data collection and storage

> - Data cleaning and storing script file location
>  ```final/data_cleaning_exploration_moviereviews.ipynb and final/data_cleaning_exploration_moviereviews.py``` script for cleaning data and storing it in .csv format. Also perform some exploratory analysis on cleaned data to verify

> - Analysis 1 script file location
>  ```final/analysis/ana_1.ipynb and final/ana_1.py``` script for analysis 1

> - Analysis 2 script file location
>  ```final/analysis/ana_2.ipynb and final/ana_2.py``` script for analysis 2

> - Analysis 3 script file location
>  ```final/analysis/ana_3.ipynb and final/ana_3.py``` script for analysis 3

> - Output files
>  ```final/analysis/ana[1-3]``` contains all the outputs in *.png* format and .csv format for analysis 1, analysis 2 and analysis 3
>  ```final/exploratory_analysis``` contains graphs plotted for exploratory analysis

-----------
Collecting and Storing Data
------------
> - Wrote *.ipynb* file to gather movie reviews data and store it in mentioned directory location.*os.path.join" is used to give a data path to save downloaded JSON files.
> - ```final/data_collection_storage_moviereviews.ipynb and final/data_collection_storage_moviereviews.py``` file is used to hit **moviereviews** api of *New York Times*.  
> - If directory path is not present creates directory path

**Logic:**
<*data_collection_storage_moviereviews.ipynb/data_collection_storage_moviereviews.py*>
> - Exported the nytimes developer api key to bash terminal and read as an *environment variable*
> - I have used **moviereviews** api to fetch data in json format
> - Defined function '''save_to_json''' for saving an object as JSON to the data directory
> - Defined function '''resolve_nyt_json''' for getting JSON, either by downloading or from a cache file. It contains check condition to avoid being rate-limited by the NYT servers and sleep after a request
> - Defined function '''get_movie_reviews_url''' which returns movie reviews url
> - Defined function '''get_movie_reviews_cache_file_path''' which returns path to store it
> - Defined function '''get_movie_reviews_params''' which returns api and offset
> - Defined functon '''resolve_movie_reviews''' for getting the result of movie reviews search
> - Provided check conditin again to check if movie has more reviews so avoid the rate limied and sleep again to download it completely.


-----------
Cleaning, Storing Data (in .csv format) and Data Exploration
------------
**Logic** **< Data cleaning and storage >**
<*data_cleaning_exploration_moviereviews.ipynb/data_cleaning_exploration_moviereviews.py*>
> - Extracted the reviews from each file in the data directory
    (default:"./data/raw_data/movie_reviews")
> - Cleaned up data in each file:
>   - Converted critics_pick to a boolean type
>   - Removed unnecessary columns ('link' and 'multimedia')
>   - Replaced opening dates of '0000-00-00' with None
>   - Punctuation is inconsistent in "byline", so removed those.Also byline are mixed case converted those to title case. Removed leading and trailing space
>   - creates year and month columns, populated first from opening_date and then from publication_date
>   - adds "Not Rated" to movies that are missing an MPAA rating
>   - Removed newlines and carriage returns from the summary
> - Combined them into a single data frame and
> - saved the combined data frame to the output file .csv
    (default:"./data/cleaned_data/movie_reviews.csv").
	
**Logic** **< Data exploration >**
<*data_cleaning_exploration_moviereviews.ipynb/data_cleaning_exploration_moviereviews.py*>
> - Read saved combined .csv into a dataframe
> - Checked shape, info of dataframe
> - Displayed 10 records using head()
> - Checked all column names of dataframe
> - Used describe() to check values inside each column
> - Displayed value counts for critics pick, mpaa rating , movie month , movie year
> - Checked number of null values present in dataframe (found that date_updated, summary_short, opening_date has some null values. We handle those if we require those columns during analysis. As of now it is fine)
> - Plotted graphs for mpaa_rating, critics_pick and publication date of reviews 
> - Defined a function "create_directory_for_output" to create output directory to save output files in .png format
> - Saved those graphs in output folder ```./exploratory_analysis```

-----------
Data Analysis - 1
------------
**Logic** 
<*ana_1.ipynb/ana_1.py*>


-----------
Data Analysis - 2 - Examine the growth of reviews by year, and see if there are any trends
------------
**Logic** 
<*ana_2.ipynb/ana_2.py*>
> - Read the cleaned combined "movie_reviews.csv" into dataframe
> - To read publication_date and date_updated properly used datatime
> - Create a dataframe containing the year and the number of movie reviews published in that perticular year
> - Defined a function "create_directory_for_output" to create output directory to save output files as .csv and .png format
> - Plotted a barplot graph using seaborn for Number of reviews per year for last 20 years and saved it to output directory in .png format
> - Saved number of reviews per year into output folder in .csv format
> - To understand trends of reviews over years , considered linear regression model 
> - Plotted linear regression output graph and saved into output folder in .png format
> - As this didn't give any significant results, plotted graph again for number of reviews from 2000 onwards with linear regression, saved graph to output folder in .png format

**Observations**
> - There is no linear increament or decreament in number of reviews over the years. 
> - linear regression model for number of reviews over all years shows that :
>    -  Coefficients: [ 4.90834732]
>    -  Variance score: 0.58
> - It means review count has no increamental growth over the years so model is perfect only approx. 58%

> - But, linear regression model for number of reviews after year 2000 onwards shows near about linear increament in no.of reviews 
>	 - Coefficients: [ 30.28360784]
>	 - Variance score: 0.80
> - It means review count has somewhat linear increamental growth after year 2000 onwards so model is perfect only approx. 80%

-----------
Data Analysis - 3 - Chi-square analysis of the distribution of critics picks: *across years*  and  *across months*
------------
**Logic** 
<*ana_3.ipynb/ana_3.py*>
> - Read the cleaned combined "movie_reviews.csv" into dataframe
> - To read publication_date and date_updated properly used datatime
> - Counted True and False critics_pick and determined probability of critics pick
> - Created a year cross tab dataframe for number of True and False critics pick over the years
> - Defined a function "create_directory_for_output" to create output directory to save output files as .csv and .png format
> - Plotted a seaborn plot to see true and false critics pick value distribution over years and saved graph in output folder in .png format
> - Saved .csv for year cross tab dataframe in output folder
> - Created empty lists to holds observed and expected value counts of critics pick
> - Calculated and displayed Chi Square value and p value from it
> - Created a month cross tab dataframe for number of True and False critics pick over the months
> - Plotted a seaborn plot to see true and false critics pick value distribution over months and saved graph in output folder in .png format
> - Saved .csv for month cross tab dataframe in output folder
> - Created empty lists to holds observed and expected value counts of critics pick
> - Created dataframe to hold months, observed and expected critics pick value
> - Saved this dataframe in .csv format in output folder
> - Plotted the chi square analysis on critics pick value distribution over month saved this graph in output folder in .png format
> - Calculated and displayed Chi Square value and p value from it

**Observations**
> - For chi square value analysis for critics pick across movie years are :
>     - Chi-square value is 1430.8100324258523
>     - p-value is 1.8123884999060126e-235
> - So, as per Chi square statistics, p value is > 0.05 , that means there is no relationship between movie year and critics pick value count. They are independant.
     
> - For chi square value analysis for critics pick across movie months are :
>     - Chi-square value is 23.488343973836614
>     - p-value is 0.015071503434154263
> - So, as per Chi square statistics, p value is < 0.05 , that means there is significant relationship between movie month and critics pick value count. They are dependant.

-----------
Output files 
------------
**Analysis 1**
<*location: /final/analysis/ana_1*>

**Analysis 2**
<*location: /final/analysis/ana_2*>
> - linear_regression_for_reviews_2000_onwards.png
> - linear_regression_for_reviews_over_all_years.png
> - Number of reviews per year for last 20 years.png
> - Number_of_reviews_per_year.csv

**Analysis 3**
<*location: /final/analysis/ana_3*>
> - Chi_square_analysis_ctritics_pick_value_over_movie_months.png
> - Crictics_pick_value_distribution_over_movie_months.png
> - Crictics_pick_value_distribution_over_movie_years.png
> - chi_square_value_over_months.csv
> - critics_value_over_months.csv
> - critics_value_over_years.csv
