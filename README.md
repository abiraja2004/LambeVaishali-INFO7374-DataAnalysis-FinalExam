Final submission : Name- Vaishali Lambe : NUID-001286444
=============================================================================================================================
-----------
Synopsis
------------
I have chosen second pattern which downloads data from NYTimes developer portal (movie reviews API), stores it and performs 3 analysis.
```final``` folder contains the following files for final exam submission:

-----------
Folder structure and locations for each file 
------------
> - Data collection and storage script location:
>  ```final/data_collection_storage_moviereviews.ipynb and final/data_collection_storage_moviereviews.py```  file to collect data and store it in a proper directory (folder) structure from NYTimes developer portal movie reviews API 

> - Raw data storage location:
>  ```final/data/raw_data/movie_reviews``` contains all JSON files for movie_reviews

> - Data cleaning and storing script file location:
>  ```final/data_cleaning_exploration_moviereviews.ipynb and final/data_cleaning_exploration_moviereviews.py``` script for cleaning data and storing it in .csv format. Also perform some exploratory analysis on cleaned data to verify

> - Cleaned data storage location:
>  ```final/data/cleaned_data``` contains cleaned data in **movie_reviews.csv** file format which is ready for analysis

> - Data analysis location:
>  ```final/analysis``` *.ipynb*  and *.py* files for analysis 1, 2 and 3 as ana_1, ana_2, ana_3 

> - Analysis 1 script file location:
>  ```final/analysis/ana_1.ipynb and final/analysis/ana_1.py``` script for analysis 1

> - Analysis 2 script file location:
>  ```final/analysis/ana_2.ipynb and final/analysis/ana_2.py``` script for analysis 2

> - Analysis 3 script file location:
>  ```final/analysis/ana_3.ipynb and final/analysis/ana_3.py``` script for analysis 3

> - Output files location:
>  ```final/analysis/ana[1-3]``` contains all the outputs in *.png* format and .csv format for analysis 1, analysis 2 and analysis 3
>  ```final/exploratory_analysis``` contains graphs plotted for exploratory analysis in .png format


-----------
Collecting and Storing Data
------------
> - Wrote *.ipynb* file to gather movie reviews data and store it in mentioned directory location.*os.path.join* is used to give a data path to save downloaded JSON files.
> - ```final/data_collection_storage_moviereviews.ipynb and final/data_collection_storage_moviereviews.py``` file is used to hit **moviereviews** API of *New York Times*.  
> - If directory path is not present it creates the directory path

**Logic:**
<*data_collection_storage_moviereviews.ipynb/data_collection_storage_moviereviews.py*>
> - Exported the NYTimes developer API key to bash terminal and read as an *environment variable*
> - I have used **moviereviews** API to fetch data in json format
> - Defined function '''save_to_json''' for saving an object as JSON to the data directory
> - Defined function '''resolve_nyt_json''' for getting JSON, either by downloading or from a cache file. It contains check condition to avoid being rate-limited by the NYT servers and sleep after a request
> - Defined function '''get_movie_reviews_url''' which returns movie reviews URL
> - Defined function '''get_movie_reviews_cache_file_path''' which returns path to store it
> - Defined function '''get_movie_reviews_params''' which returns API and offset
> - Defined function '''resolve_movie_reviews''' for getting the result of movie reviews search
> - Provided check condition again to check if movie has more reviews so avoid the rate limit and sleep again to download it completely.


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
>   - Punctuation is inconsistent in "byline", so removed those. Also byline are mixed case converted those to title case. Removed leading and trailing space
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
     - ![Distribution_of_mpaa_rating1](https://github.com//vaishalilambe/LambeVaishali-INFO7374-DataAnalysis-FinalExam/tree/master/final/exploratory_analysis/Distribution_of_mpaa_rating1.png)
	 - ![Distribution_of_mpaa_rating2](https://github.com//vaishalilambe/LambeVaishali-INFO7374-DataAnalysis-FinalExam/tree/master/final/exploratory_analysis/Distribution_of_mpaa_rating2.png)
	 - ![critic_pick_value_count](https://github.com//vaishalilambe/LambeVaishali-INFO7374-DataAnalysis-FinalExam/tree/master/final/exploratory_analysis/critic_pick_value_count.png)
	 - ![Review_count_pubicationdates](https://github.com//vaishalilambe/LambeVaishali-INFO7374-DataAnalysis-FinalExam/tree/master/final/exploratory_analysis/Review_count_pubicationdates.png)
> - Defined a function "create_directory_for_output" to create output directory to save output files in .png format
> - Saved those graphs in output folder ```./exploratory_analysis```


-----------
Data Analysis - 1 - Zipf's Law on summaries column of movie reviews - do the words used there follow Zipf's Law?
------------
**Logic** 
<*ana_1.ipynb/ana_1.py*>
> - Imported required modules
> - Checked if movie_reviews.csv file is present at given location or not, if not displayed error message to run cleaning data script
> - Read the cleaned combined "movie_reviews.csv" into dataframe
> - Defined a function "is_desirable_word" to remove punctuations, single digits, numbers, odd ones etc.
> - Defined a function "remove_html_entities" to remove html entities
> - Defined a function "split_lines_into_words" to split review text line to words
> - Created lists for all words, all vocab, interesting words and interesting vocab
> - Calculated frequency distribution for the interesting words
> - Displayed most common words from review text words
> - Created frequency list and sorted it from high to low
> - Created word rank frequency
> - Defined a function "create_csv" to save words, rank and frequency in .csv file
> - Saved .csv in output folder as "Zipfs_law_review_text.csv"
> - Plotted word rank and frequency relationship in log-log plot using matplotlib 
> - Saved it into output folder as .png format 
	 - ![Zipfs_law_review_summeries](https://github.com//vaishalilambe/LambeVaishali-INFO7374-DataAnalysis-FinalExam/tree/master/final/analysis/ana_1/Zipfs_law_review_summeries.png)

**Observations**
> - The field that this set of words comes from (movie reviews) is really obvious when looking at the 10 most common words:
	 - film
	 - movie
	 - comedy
	 - documentary
	 - drama
	 - story
> - log-log plot shows that review summary text words and frequency product is constant for majority of words ,though it is not true for all the words.
	Hence zipf's law holds true for most of the review summary words.
	
	
-----------
Data Analysis - 2 - Examine the growth of reviews by year, and see if there are any trends
------------
**Logic** 
<*ana_2.ipynb/ana_2.py*>
> - Imported required modules
> - Checked if movie_reviews.csv file is present at given location or not, if not displayed error message to run cleaning data script
> - Read the cleaned combined "movie_reviews.csv" into dataframe
> - To read publication_date and date_updated properly used datatime
> - Create a dataframe containing the year and the number of movie reviews published in that particular year
> - Defined a function "create_directory_for_output" to create output directory to save output files as .csv and .png format
> - Plotted a barplot graph using seaborn for Number of reviews per year for last 20 years and saved it to output directory in .png format
     - ![number_of_reviews_per_year_last_20years](https://github.com//vaishalilambe/LambeVaishali-INFO7374-DataAnalysis-FinalExam/tree/master/final/analysis/ana_2/number_of_reviews_per_year_for_last_20years.png)
> - Saved number of reviews per year into output folder in .csv format
> - To understand trends of reviews over years, considered linear regression model 
> - Plotted linear regression output graph and saved into output folder in .png format
	 - ![linear_regression_moviereviews_years](https://github.com//vaishalilambe/LambeVaishali-INFO7374-DataAnalysis-FinalExam/tree/master/final/analysis/ana_2/linear_regression_for_reviews_over_all_years.png)	
> - As this didn't give any significant results, plotted graph again for number of reviews from 2000 onwards with linear regression, saved graph to output folder in .png format
	 - ![linear_regression_moviereviews_2000_onwards](https://github.com//vaishalilambe/LambeVaishali-INFO7374-DataAnalysis-FinalExam/tree/master/final/analysis/ana_2/linear_regression_for_reviews_2000_onwards.png)

**Observations**
> - There is no linear increment or decrement in number of reviews over the years. 
> - linear regression model for number of reviews over all years shows that :
>    -  Coefficients: [ 4.90834732]
>    -  Variance score: 0.58
> - It means review count has no incremental growth over the years so model is perfect only approx. 58%

> - But, linear regression model for number of reviews after year 2000 onwards shows near about linear increment in number of reviews 
>	 - Coefficients: [ 30.28360784]
>	 - Variance score: 0.80
> - It means review count has somewhat linear incremental growth after year 2000 onwards so model is perfect only approx. 80%


-----------
Data Analysis - 3 - Chi-square analysis of the distribution of critic's picks: *across years*, *across months*,*across critics* and *across MPAA ratings*
------------
**Logic** 
<*ana_3.ipynb/ana_3.py*>
> - Imported required modules
> - Checked if movie_reviews.csv file is present at given location or not, if not displayed error message to run cleaning data script
> - Read the cleaned combined "movie_reviews.csv" into dataframe
> - To read publication_date and date_updated properly used datatime
> - Counted True and False critics_pick and determined probability of critic's pick
> - Created a year cross tab dataframe for number of True and False critic's pick over the years
> - Calculated critics pick value overall probability
> - Defined a function "create_directory_for_output" to create output directory to save output files as .csv and .png format
> - Plotted a seaborn plot to see true and false critics pick value distribution over years and saved graph in output folder in .png format
	![critics_pick_value_distribution_over_movie_years](https://github.com//vaishalilambe/LambeVaishali-INFO7374-DataAnalysis-FinalExam/tree/master/final/analysis/ana_3/critics_pick_value_distribution_over_movie_years.png)
> - Saved .csv for year cross tab dataframe in output folder (name of the file: years_cross_tab.csv)
> - Defined a function to calculate chi-square value, which takes dataframe and critics pick as input and returns observed, expected, chisquare_value, pvalue
> - Calculated and displayed Chi Square value and p value from it
> - Created a month cross tab dataframe for number of True and False critic's pick over the months
> - Plotted a seaborn plot to see true and false critic's pick value distribution over months and saved graph in output folder in .png format
	![critics_pick_value_distribution_over_movie_months](https://github.com//vaishalilambe/LambeVaishali-INFO7374-DataAnalysis-FinalExam/tree/master/final/analysis/ana_3/critics_pick_value_distribution_over_movie_months.png)
> - Saved .csv for month cross tab dataframe in output folder( name of the file: month_cross_tab.csv)
> - Created empty lists to holds observed and expected value counts of critic's pick
> - Created dataframe to hold months, observed and expected critic's pick value
> - Saved this dataframe in .csv format in output folder ( name of file: critics_pick_value_over_months_observed_expected.csv)
> - Plotted the chi square analysis on critic's pick value distribution over month and saved this graph in output folder in .png format
	![chi_square_analysis_critics_pick_value_by_movie_months](https://github.com//vaishalilambe/LambeVaishali-INFO7374-DataAnalysis-FinalExam/tree/master/final/analysis/ana_3/chi_square_analysis_critics_pick_value_by_movie_months.png)
> - Calculated and displayed Chi Square value and p value from it
> - To get more insight on analysis plotted a factor plot for observed and expected ctitics pick value over months
	![chi_square_analysis_critics_pick_value_over_months](https://github.com//vaishalilambe/LambeVaishali-INFO7374-DataAnalysis-FinalExam/tree/master/final/analysis/ana_3/nested_barplot_critics_pick_by_month.png)
> - Saved it to output folder as .png (name of file: nested_barplot_critics_pick_by_month.png)
> - To get more insights to critic pick value distribution plotted factorplots for differnet year ranges and saved those as .png
    ![critics_pick_value_from_1915_to_1933](https://github.com//vaishalilambe/LambeVaishali-INFO7374-DataAnalysis-FinalExam/tree/master/final/analysis/ana_3/critics_pick_value_from_1915_to_1933.png)
	![critics_pick_value_from_1934_to_1948](https://github.com//vaishalilambe/LambeVaishali-INFO7374-DataAnalysis-FinalExam/tree/master/final/analysis/ana_3/critics_pick_value_from_1934_to_1948.png)
	![critics_pick_value_from_1949_to_1963](https://github.com//vaishalilambe/LambeVaishali-INFO7374-DataAnalysis-FinalExam/tree/master/final/analysis/ana_3/critics_pick_value_from_1949_to_1963.png)
	![critics_pick_value_from_1964_to_1978](https://github.com//vaishalilambe/LambeVaishali-INFO7374-DataAnalysis-FinalExam/tree/master/final/analysis/ana_3/critics_pick_value_from_1964_to_1978.png)
	![critics_pick_value_from_1979_to_1993](https://github.com//vaishalilambe/LambeVaishali-INFO7374-DataAnalysis-FinalExam/tree/master/final/analysis/ana_3/critics_pick_value_from_1979_to_1993.png)
	![critics_pick_value_from_1994_to_2008](https://github.com//vaishalilambe/LambeVaishali-INFO7374-DataAnalysis-FinalExam/tree/master/final/analysis/ana_3/critics_pick_value_from_1994_to_2008.png)
	![critics_pick_value_from_2009_to_2017](https://github.com//vaishalilambe/LambeVaishali-INFO7374-DataAnalysis-FinalExam/tree/master/final/analysis/ana_3/critics_pick_value_from_2009_to_2017.png)

> - After few observations from a graph divided data into pre 1998 and post 1998 for years and calculated chi square value in each case
> - Plotted nested bar plots for pre 1998 and post 1998 to analyse more and saved those as .png file in output folder. Also populated critic pick probability pre 1998 and post 1998
	![nested_barplot_critics_pick_by_year_pre_1998](https://github.com//vaishalilambe/LambeVaishali-INFO7374-DataAnalysis-FinalExam/tree/master/final/analysis/ana_3/nested_barplot_critics_pick_by_year_pre_1998.png)
	![nested_barplot_critics_pick_by_year_post_1998](https://github.com//vaishalilambe/LambeVaishali-INFO7374-DataAnalysis-FinalExam/tree/master/final/analysis/ana_3/nested_barplot_critics_pick_by_year_post_1998.png)
> - Performed chi square value analysis for pre 1998 years and post 1998 years 
> - Counted reviews and displayed top 20 critics as well as critics who have written more than 10 reviews
> - Created normal dataframe for critics
> - Calculated top critics pick probability
> - Created top critics cross tab dataframe and analysed chi squqare and p values
> - similary for mpaa rating , created cross tab, calculated chi square and p value
> - Plotted factorplot to see observed and expected pick value distribution across mpaa rating
> - Saved output in output folder as .png format
	![nested_barplot_critics_pick_by_mpaa_rating](https://github.com//vaishalilambe/LambeVaishali-INFO7374-DataAnalysis-FinalExam/tree/master/final/analysis/ana_3/nested_barplot_critics_pick_by_mpaa_rating.png)

**Observations**
> - Critic's Pick overall probability is:  0.116275610754, which shows that overall chance that a random movie review from the New York Times had a Critic's   	Pick associated with it is 11.6%, or approximately 1 in 9
> - *across year and month*
> - For chi square value analysis for critic's pick across movie years are :
>     - Chi-square value is 1430.8100324258523
>     - p-value is 1.8123884999060126e-235
> - So, as per chi-square statistics, p value is < 0.05, which means that it is statistically unlikely this distribution occurred by chance. We conclude that the number of Critic's Picks are not evenly distributed among the years.     
> - For chi square value analysis for critic's pick across movie months are :
>     - Chi-square value is 23.488343973836614
>     - p-value is 0.015071503434154263
> - So, as per chi-square statistics, p value is < 0.05, which means that it is statistically unlikely this distribution occurred by chance. We conclude that the number of Critic's Picks are not evenly distributed among the months.
> - From nested_barplot.crictics_pick_by_month.png found that:
	  - The number of actual Critic's Picks is lower than expected during January through to May, and higher than expected from July to December (with the   exception of August).
      - The biggest discrepancy occurs during December, when the number of Critic's Picks is nearly 25% higher than expected.
      - The biggest discrepancy going the other way occurs in April, when the number of Critic's Picks is 13% lower than expected.
> - From various graphs plotted for critic value distribution for observed and expected values we found that:
	  - Historically, the number of Critic's Picks is consistently below the expected value until 1998, when there is a huge (relative) increase. There appear to be 2 distinct regions here: [1914 - 1997] and [1998 onwards].
> - Explanations could come from a couple of places:
      - External: did the quality of moviemaking increase dramatically from 1998 onwards, thus justifying the increased number of Critic's Picks?
      - Internal: was there an organisational change at the New York Times that caused a deliberate increase in the proportion of Critic's Picks? Perhaps change in the movie review staff, or a change in methodology to only review "higher-quality" movies? Or, more cynically, did the organisation have a monetary incentive to promote movies more heavily, such as an investment by the parent company into the film industry or the purchase of shares in a chain of theatres?
> - The chi-square values are greatly reduced for each region:
     - for all years the chi-square value was 1430.81, and the p-value was 1.81e-235
     - pre-1998 the chi-square value is 228.10, and the p-value is 1.24e-16
     - post-1998 the chi-square value is 93.51, and the p-value is 7.86e-12
     - But the p-value is still so small that there is a negligible chance that the Critic's Pick choices are compatible with a random selection.
> - There is a huge change in the proportion of films rated as Critic's Pick pre- and post-1998.
     - Before 1998, 6% of films were Critic's Picks.
     - But then from 1998 onwards, over 20% of films were Critic's Picks.

> - *across critics*	 
> -  Top 20 critics:
	['Bosley Crowther', 'Stephen Holden', 'Janet Maslin', 'Vincent Canby', 'A O Scott', 'Mordaunt Hall', 'Jeannette Catsoulis', 'Manohla Dargis', 'Neil Genzlinger', 'Howard Thompson', 'Caryn James', 'Frank S Nugent', 'Elvis Mitchell', 'A H Weiler', 'Lawrence Van Gelder', 'Andy Webster', 'Nicolas Rapold', 'Roger Greenspun', 'T M P', 'A W']
> - Total number of critics with 10 or more reviews: 71
> - Top critics: chi-square = 1688.9738104239152, pvalue = 1.121251558769804e-303

> - *across mpaa rating*
> - MPAA ratings: chi-square = 109.79994917608118, pvalue = 2.244792308406809e-21
     - The chi-square value is considerably lower than for the top critics (1690) or years (1431).
     - The Critic's Picks might be more evenly distributed by MPAA rating than across the other axes, but the p-value still indicates that the discrepancy there didn't arise by chance.	 
> - The expected and observed values are very good for G, NC-17, PG, PG-13 and X rated movies.
> - There are fewer Critic's Picks for Not Rated movies than expected, and more than expected for R rated movies.

> - Speculation
	 - Not Rated movies probably cover many independent and film festival type movies, and as such their overall quality could be less than bigger budget movies from major studios.
	 - R rated movies can cover grittier material, so perhaps it is more likely that the emotionally moving and realistic movies that a critic would recommend highly are rated R.
> - At any rate, the discrepancy between observed and expected numbers of Critic's Picks is not as great across MPAA ratings as it is across critics and years.


-----------
Output files 
------------
**Analysis 1**
<*location: /final/analysis/ana_1*>
> - Zipfs_law_review_summeries.png
> - Zipfs_law_review_text.csv

**Analysis 2**
<*location: /final/analysis/ana_2*>
> - linear_regression_for_reviews_2000_onwards.png
> - linear_regression_for_reviews_over_all_years.png
> - number_of_reviews_per_year_for_last_20years.png
> - Number_of_reviews_per_year.csv

**Analysis 3**
<*location: /final/analysis/ana_3*>
> - chi_square_analysis_critics_pick_value_by_movie_months.png
> - critics_pick_value_distribution_over_movie_months.png
> - critics_pick_value_distribution_over_movie_years.png
> - critics_pick_value_from_1915_to_1933.png
> - critics_pick_value_from_1934_to_1948.png
> - critics_pick_value_from_1949_to_1963.png
> - critics_pick_value_from_1964_to_1978.png
> - critics_pick_value_from_1979_to_1993.png
> - critics_pick_value_from_1994_to_2008.png
> - critics_pick_value_from_2009_to_2017.png
> - nested_barplot_critics_pick_by_month.png
> - nested_barplot_critics_pick_by_mpaa_rating.png
> - nested_barplot_critics_pick_by_year_post_1998.png
> - nested_barplot_critics_pick_by_year_pre_1998.png
> - chi_square_value_over_months.csv
> - critics_pick_value_over_months_observed_expected.csv
> - month_cross_tab.csv
> - years_cross_tab.csv


-----------
Instructions to run
------------
> - Go to directory where .py file is pressent on any git bash/terminal shell
> - Run below command
	python<space><filename>.py <hit enter>
	e.g. python ana_1.py

-----------
Glossary of some important terms used
------------
> - Zipf's law: states that given a large sample of words used, the frequency of any word is inversely proportional to its rank in the frequency table
> - Linear regression model:  an approach for modeling the relationship between a scalar dependent variable y and one or more explanatory variables (or independent variables) denoted X
> - Chi Square analysis: determines whether there is a significant association between the two variables
> - p-value: a number between 0 and 1 and interpreted in the following way: A small p-value (typically ≤ 0.05) indicates strong evidence against the null hypothesis, so you reject the null hypothesis
> - Critics pick: critics on blockbusters, independents and everything in between
> - MPAA rating: The Motion Picture Association of America (MPAA) film rating system is used in the United States and its territories to rate a film's suitability for certain audiences based on its content.
	 - G:General Audiences
	 - PG: Parental Guidance Suggested
	 - PG-13: Parents Strongly Cautioned
	 - R – Restricted
	 - NC-17: Adults Only
> - crosstab(pandas crosstab) : Compute a simple cross-tabulation of two (or more) factors. By default computes a frequency table of the factors unless an array of values and an aggregation function are passed
