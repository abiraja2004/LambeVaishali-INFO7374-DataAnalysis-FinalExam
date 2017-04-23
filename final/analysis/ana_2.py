# Import modules needed
import numpy as np
import pandas as pd
import os
from sklearn import linear_model
import seaborn as sns
sns.set(style='white',color_codes=True)
import matplotlib.pyplot as plt
#%atplotlib inline

# Path to the data directory into which the cleaned data is saved.
csv_file_path = os.path.join("..", "data", "cleaned_data", "movie_reviews.csv")
if not os.path.exists(csv_file_path):
    print("{} doesn't exist - perhaps the data cleaning script needs to be run?".format(csv_file_path))
	
# read 'movie_reviews.csv' into a dataframe
review_df = pd.read_csv(csv_file_path, quoting=2, parse_dates=True, infer_datetime_format=True, encoding="UTF-8")

# These don't get read back properly as dates :(
review_df['publication_date'] = pd.to_datetime(review_df['publication_date'])
review_df['date_updated'] = pd.to_datetime(review_df['date_updated'])

# create a list to hold the years
year_list = []

for y in review_df['movie_year'].unique():
    count = len(review_df[review_df['movie_year'] == y]['movie_year'])    
    year_list.append({'year':int(y), 'count':count})
    
reviews_by_year = pd.DataFrame.from_records(year_list, columns=['year', 'count'])
reviews_by_year.sort_values('year', axis=0, ascending=True, inplace=True)
reviews_by_year = reviews_by_year.reset_index(drop=True)

# Drop 2017, since it isn't a complete year.
reviews_by_year = reviews_by_year[reviews_by_year['year'] != 2017]

# Drop 2005, since having 10 reviews is suspicious (2004 had 278, 2006 had 419).
reviews_by_year = reviews_by_year[reviews_by_year['year'] != 2005]

#Function to create output data folder to store graph and .csv 
def create_directory_for_output():
    current_dir = os.path.dirname('__file__')
    data_folder = os.path.join(current_dir, 'ana_2')
    if not os.path.exists(data_folder):
        os.mkdir(data_folder)
    return data_folder

output_folder=create_directory_for_output()

# plot barplot graph using seaborn for Number of reviews per year for last 20 years
sns.set_style("whitegrid")
plt.figure(figsize=(14, 8))
ax = sns.barplot(x="year", y="count",data=reviews_by_year.tail(20));
plt.title('Number of reviews per year for last 20 years')
sns.set(font_scale=1.5)
plt.show()

# save the plot to output folder
plot_name = 'number_of_reviews_per_year_for_last_20years'
plot_path = os.path.join(output_folder, plot_name)
plot_path+='.png'
ax.figure.savefig(plot_path,bbox_inches='tight')

#csv file name and path
file_name = 'Number_of_reviews_per_year'
file_path = os.path.join(output_folder, file_name)
file_path+='.csv'

#Save file to created output file
reviews_by_year.to_csv(file_path,index = False)

# check linear regression model to understand trends og number of reviews per year
x_data = reviews_by_year['year'].values.reshape(-1, 1)
y_data = reviews_by_year['count']

regr = linear_model.LinearRegression()
fit = regr.fit(x_data, y_data)

# The coefficients.
print('Coefficients: \n', regr.coef_)

# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % regr.score(x_data, y_data))

# Plot outputs
plt.title('linear_regression_for_reviews_over_all_years')
ax=plt.scatter(x_data, y_data, color='black')
plt.plot(x_data, regr.predict(x_data), color='blue', linewidth=3)

# show the plot
plt.show()

# save the plot to output folder
plot_name = 'linear_regression_for_reviews_over_all_years'
plot_path = os.path.join(output_folder, plot_name)
plot_path+='.png'
ax.figure.savefig(plot_path,bbox_inches='tight')

# Only consider reviews for year greater than or equal to 2000
recent_reviews = reviews_by_year[reviews_by_year['year'] >= 2000]


x_data = recent_reviews['year'].values.reshape(-1, 1)
y_data = recent_reviews['count']

# Applying linear regression
regr = linear_model.LinearRegression()
fit = regr.fit(x_data, y_data)

# The coefficients.
print('Coefficients: \n', regr.coef_)

# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % regr.score(x_data, y_data))

# Plot outputs.
plt.title('linear_regression_for_reviews_2000_onwards')
ax=plt.scatter(x_data, y_data, color='black')
plt.plot(x_data, regr.predict(x_data), color='red', linewidth=3)
plt.show()

# save the plot to output folder
plot_name = 'linear_regression_for_reviews_2000_onwards'
plot_path = os.path.join(output_folder, plot_name)
plot_path+='.png'
ax.figure.savefig(plot_path,bbox_inches='tight')


