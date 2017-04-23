# Import modules needed 
import numpy as np
import pandas as pd
import os
from sklearn import linear_model
from scipy.stats import chisquare
import seaborn as sns
sns.set(style='white',color_codes=True)
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Path to the data directory into which the cleaned data is saved.
csv_file_path = os.path.join("..", "data", "cleaned_data", "movie_reviews.csv")
if not os.path.exists(csv_file_path):
    print("{} doesn't exist - perhaps the data cleaning script needs to be run?".format(csv_file_path))
	
# read movie_reviews.csv as dataframe
review_df = pd.read_csv(csv_file_path, quoting=2, parse_dates=True, infer_datetime_format=True, encoding="UTF-8")

# These don't get read back properly as dates :(
review_df['publication_date'] = pd.to_datetime(review_df['publication_date'])
review_df['date_updated'] = pd.to_datetime(review_df['date_updated'])

# See how many of these there are - this establishes the base probability of a movie being a "Critic's Pick".
print("Critic's Pick value count is:")
print(review_df['critics_pick'].value_counts())
      
# get the count for Critic's Pick 
cp_true = review_df[review_df['critics_pick'] == True]['critics_pick'].count()
cp_false = review_df[review_df['critics_pick'] == False]['critics_pick'].count()

# get probability of Critic's Pick
critics_pick_probability = cp_true / (cp_true + cp_false)
print("Critic's Pick overall probability is: ", critics_pick_probability)

# create a year cross tab dataframe for number of True and False Critic's Pick over the years
year_crosstab_df = pd.crosstab(review_df.critics_pick, review_df.movie_year)

# Function to create output data folder
def create_directory_for_output():
    current_dir = os.path.dirname('__file__')
    data_folder = os.path.join(current_dir, 'ana_3')
    if not os.path.exists(data_folder):
        os.mkdir(data_folder)
    return data_folder

output_folder = create_directory_for_output()

# plot a seaborn plot to see true and false Critic's Pick value distribution over years
sns.set_style("whitegrid")
plt.figure(figsize=(14, 10))
ax = sns.violinplot(x="critics_pick", y="movie_year", data=review_df, split=True);
plt.title("Critic's Pick value distribution over movie years")
sns.set(font_scale=1.5)
plt.show()

# save the plot in output folder
plot_name = 'critics_pick_value_distribution_over_movie_years.png'
plot_path = os.path.join(output_folder, plot_name)

ax.figure.savefig(plot_path, bbox_inches='tight')

#csv file name and path
file_name = 'years_cross_tab.csv'
file_path = os.path.join(output_folder, file_name)

#Save file to created output file
year_crosstab_df.to_csv(file_path, index = True)

# Calculate the chi-square value given a dataframe and Critic's Pick probability.
#
# df - dataframe to use
# cp_probability - probability that a movie is a Critic's Pick
#
# returns - observed counts, expected counts, chi-square value and p-value
def calculate_chisquare(df, cp_probability, verbose=False):
    # create lists observed and expected to hold values for observed and expected 
    observed = []
    expected = []
    for y in df.columns:
        exp = df[y].sum() * cp_probability
        obs = df[y][True]
        
        if verbose:
            print("{} -> {} vs {:.02f}".format(y, obs, exp))

        expected.append(exp)
        observed.append(obs)

    observed = np.array(observed)
    expected = np.array(expected)
    chisquare_value, pvalue = chisquare(observed, expected)
    
    return observed, expected, chisquare_value, pvalue
	
# chi square value and p value calculation
observed, expected, chisquare_value, pvalue = calculate_chisquare(year_crosstab_df, 
                                                                  critics_pick_probability, 
                                                                  verbose=True)

# display chi square value and p value for Critic's Pick value distribution over all the years
print("Chi-square value is {}".format(chisquare_value))
print("p-value is {}".format(pvalue))

# create a month cross tab for Critic's Pick value over the movie months
month_crosstab_df = pd.crosstab(review_df.critics_pick, review_df.movie_month_name)

# Reorder into chronological order.
month_crosstab_df = month_crosstab_df[['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']]

# plot a seaborn plot to see critics pick value distribution over movie months
sns.set_style("whitegrid")
plt.figure(figsize=(14, 8))
ax = sns.violinplot(x="movie_month", y="critics_pick", data=review_df, split=True);
plt.title('Critics Pick value distribution over months')
sns.set(font_scale=1.5)
plt.show()

# save the plot in output folder
plot_name = 'critics_pick_value_distribution_over_movie_months.png'
plot_path = os.path.join(output_folder, plot_name)
ax.figure.savefig(plot_path, bbox_inches='tight')

#csv file name and path
file_name = 'month_cross_tab.csv'
file_path = os.path.join(output_folder, file_name)

#Save file to created output file
month_crosstab_df.to_csv(file_path,index = True)

# create lists observed and expected to hold values for observed and expected 
observed, expected, chisquare_value, pvalue = calculate_chisquare(month_crosstab_df, critics_pick_probability)

# create a dataframe to hold month, expected and observed critic pick values
se = pd.Series(observed)
month_chi_df = pd.DataFrame()
obs = pd.Series(observed)
exp = pd.Series(expected)
month_chi_df['movie_month'] = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
month_chi_df['observed_critics_pick_value'] = obs.values
month_chi_df['expected_critics_pick_value'] = exp.values
month_chi_df

#csv file name and path
file_name = 'critics_pick_value_over_months_observed_expected.csv'
file_path = os.path.join(output_folder, file_name)

#Save file to created output file
month_chi_df.to_csv(file_path,index = True)

# Plot the chi square value distribution over month
sns.set_style("whitegrid")

# 2 Box plots to generate expected and observed chi square values over month
fig = plt.figure(figsize=(14,8))
bx = sns.barplot(x='movie_month', y='expected_critics_pick_value', data=month_chi_df, color='blue')
bx = sns.barplot(x='movie_month', y='observed_critics_pick_value', data=month_chi_df, color='red')

# To generate custom legends
expected = mpatches.Patch(color='blue', label='Expected value')
observed = mpatches.Patch(color='red', label='Observed value')

# Beautify plot
bx.legend(handles=[expected, observed], bbox_to_anchor=(1.05, 1), loc=2)
plt.suptitle('Chi-square analysis for critics pick value by movie month')
bx.set(xlabel='Month', ylabel="Critic's Pick value count")
plt.show()

# save the graph 
plot_filename = 'chi_square_analysis_critics_pick_value_by_movie_months.png'
plot_path = os.path.join(output_folder, plot_filename)
fig.savefig(plot_path, bbox_inches='tight')

print("Chi-square value is {}".format(chisquare_value))
print("p-value is {}".format(pvalue))

# Rearrange the data into a format suitable for sns.factorplot().

# Create a dataframe for the expected values, with columns [month, critics_pick, Source='Expected'].
expected_df = month_chi_df.copy()
expected_df.rename(columns={'expected_critics_pick_value':'critics_pick', 'movie_month':'month'}, inplace=True)
expected_df.drop('observed_critics_pick_value', axis=1, inplace=True)
expected_df['Source'] = 'Expected'

# Create a dataframe for the observed values, with columns [month, critics_pick, Source='Observed'].
observed_df = month_chi_df.copy()
observed_df.drop('expected_critics_pick_value', axis=1, inplace=True)
observed_df.rename(columns={'observed_critics_pick_value':'critics_pick', 'movie_month':'month'}, inplace=True)
observed_df['Source'] = 'Observed'

# Combine the 2 sub-dataframes.
month_barplot_df = pd.concat([expected_df, observed_df], axis=0)
#print(month_barplot_df.info())
#print(month_barplot_df.head(24))


# Draw a nested barplot to show Critic's Pick for month and observed/expected.
fig = plt.figure(figsize=(14,8))

factorplot = sns.factorplot(x="month", y='critics_pick', data=month_barplot_df, 
                   hue="Source", size=12, kind="bar", palette="muted")
factorplot.despine(left=True)
plt.title("nested_barplot_critics_pick_by_month")
factorplot.set_xlabels("Month")
factorplot.set_ylabels("Number of Critic's Picks")
#factorplot.set_title("Title goes here")
plt.show()

# save the graph 
plot_filename = 'nested_barplot_critics_pick_by_month.png'
plot_path = os.path.join(output_folder, plot_filename)
factorplot.savefig(plot_path, bbox_inches='tight')

# Rearrange the data into a format suitable for sns.factorplot().
def create_year_factorplot_df(df, cp_probability):
    year_nested_barplot_list = []
    for y in df['movie_year'].unique():
        movie_count = df[df['movie_year'] == y].shape[0]
        cp_count = df[(df['movie_year'] == y) & (df['critics_pick'] == True)].shape[0]
        expected_count = movie_count * cp_probability

        #print("{}: {} out of {}, expected {}".format(y, cp_count, movie_count, expected_count))

        year_nested_barplot_list.append({'year':y, 'critics_pick':cp_count, 'Source':'Observed'})
        year_nested_barplot_list.append({'year':y, 'critics_pick':expected_count, 'Source':'Expected'})

    # Create a dataframe for the values, with columns [month, critics_pick, Source].
    result_df = pd.DataFrame.from_records(year_nested_barplot_list, columns=['year', 'critics_pick', 'Source'])
    result_df.sort_values('year', axis=0, ascending=True, inplace=True)
    result_df = result_df.reset_index(drop=True)

    return result_df

year_barplot_df = create_year_factorplot_df(review_df, critics_pick_probability)
#print(year_barplot_df.info())
#print(year_barplot_df.head(24))


# Draw a nested barplot to show Critic's Pick for year and observed/expected.
fig = plt.figure(figsize=(14,8))

factorplot = sns.factorplot(x="year", y='critics_pick', data=year_barplot_df[:30], 
                   hue="Source", size=12, kind="bar", palette="muted")
plt.title(" critics_pick_value_from_1915_to_1933")
factorplot.despine(left=True)
factorplot.set_xlabels("Year")
factorplot.set_ylabels("Number of Critic's Picks")
plt.show()

# save the graph 
plot_filename = 'critics_pick_value_from_1915_to_1933.png'
plot_path = os.path.join(output_folder, plot_filename)
factorplot.savefig(plot_path, bbox_inches='tight')

factorplot = sns.factorplot(x="year", y='critics_pick', data=year_barplot_df[31:60], 
                   hue="Source", size=12, kind="bar", palette="muted")
plt.title(" critics_pick_value_from_1934_to_1948")
factorplot.despine(left=True)
factorplot.set_xlabels("Year")
factorplot.set_ylabels("Number of Critic's Picks")
plt.show()

# save the graph 
plot_filename = 'critics_pick_value_from_1934_to_1948.png'
plot_path = os.path.join(output_folder, plot_filename)
factorplot.savefig(plot_path, bbox_inches='tight')

factorplot = sns.factorplot(x="year", y='critics_pick', data=year_barplot_df[61:90], 
                   hue="Source", size=12, kind="bar", palette="muted")
plt.title(" critics_pick_value_from_1949_to_1963")
factorplot.despine(left=True)
factorplot.set_xlabels("Year")
factorplot.set_ylabels("Number of Critic's Picks")
plt.show()

# save the graph 
plot_filename = 'critics_pick_value_from_1949_to_1960.png'
plot_path = os.path.join(output_folder, plot_filename)
factorplot.savefig(plot_path, bbox_inches='tight')

factorplot = sns.factorplot(x="year", y='critics_pick', data=year_barplot_df[91:120], 
                   hue="Source", size=12, kind="bar", palette="muted")
plt.title(" critics_pick_value_from_1964_to_1978")
factorplot.despine(left=True)
factorplot.set_xlabels("Year")
factorplot.set_ylabels("Number of Critic's Picks")
plt.show()

# save the graph 
plot_filename = 'critics_pick_value_from_1964_to_1978.png'
plot_path = os.path.join(output_folder, plot_filename)
factorplot.savefig(plot_path, bbox_inches='tight')

factorplot = sns.factorplot(x="year", y='critics_pick', data=year_barplot_df[121:150], 
                   hue="Source", size=12, kind="bar", palette="muted")
plt.title(" critics_pick_value_from_1979_to_1993")
factorplot.despine(left=True)
factorplot.set_xlabels("Year")
factorplot.set_ylabels("Number of Critic's Picks")
plt.show()

# save the graph 
plot_filename = 'critics_pick_value_from_1979_to_1993.png'
plot_path = os.path.join(output_folder, plot_filename)
factorplot.savefig(plot_path, bbox_inches='tight')

factorplot = sns.factorplot(x="year", y='critics_pick', data=year_barplot_df[151:180], 
                   hue="Source", size=12, kind="bar", palette="muted")
plt.title(" critics_pick_value_from_1994_to_2008")
factorplot.despine(left=True)
factorplot.set_xlabels("Year")
factorplot.set_ylabels("Number of Critic's Picks")
plt.show()

# save the graph 
plot_filename = 'critics_pick_value_from_1994_to_2008.png'
plot_path = os.path.join(output_folder, plot_filename)
factorplot.savefig(plot_path, bbox_inches='tight')

factorplot = sns.factorplot(x="year", y='critics_pick', data=year_barplot_df[181:], 
                   hue="Source", size=12, kind="bar", palette="muted")
plt.title(" critics_pick_value_from_2009_to_2016")
factorplot.despine(left=True)
factorplot.set_xlabels("Year")
factorplot.set_ylabels("Number of Critic's Picks")
plt.show()

# save the graph 
plot_filename = 'critics_pick_value_from_2009_to_20.png'
plot_path = os.path.join(output_folder, plot_filename)
factorplot.savefig(plot_path, bbox_inches='tight')

# Pre-1998.
pre_1998_df = review_df[review_df['movie_year'] < 1998].copy()

print("Pre-1998 Critic's Pick value count is:\n{}".format(pre_1998_df['critics_pick'].value_counts()))
      
# get the count for Critic's Pick 
pre_1998_cp_true = pre_1998_df[pre_1998_df['critics_pick'] == True]['critics_pick'].count()
pre_1998_cp_false = pre_1998_df[pre_1998_df['critics_pick'] == False]['critics_pick'].count()

# get probability of Critic's Pick
pre_1998_critics_pick_probability = pre_1998_cp_true / (pre_1998_cp_true + pre_1998_cp_false)
print("Pre-1998 Critic's Pick probability is: ", pre_1998_critics_pick_probability)


# 1998 and onwards.
post_1998_df = review_df[review_df['movie_year'] >= 1998].copy()

print("Post-1998 Critic's Pick value count is:\n{}".format(post_1998_df['critics_pick'].value_counts()))
      
# get the count for Critic's Pick
post_1998_cp_true = post_1998_df[post_1998_df['critics_pick'] == True]['critics_pick'].count()
post_1998_cp_false = post_1998_df[post_1998_df['critics_pick'] == False]['critics_pick'].count()

# get probability of Critic's Pick
post_1998_critics_pick_probability = post_1998_cp_true / (post_1998_cp_true + post_1998_cp_false)
print("Post-1998 Critic's Pick probability is: ", post_1998_critics_pick_probability)

# create a pre-1998 cross tab dataframe for number of True and False Critic's Pick over the years
pre_1998_crosstab_df = pd.crosstab(pre_1998_df.critics_pick, pre_1998_df.movie_year)

pre_1998_observed, pre_1998_expected, pre_1998_chisquare_value, pre_1998_pvalue = calculate_chisquare(pre_1998_crosstab_df, pre_1998_critics_pick_probability)
print("Pre-1998: chi-square = {}, pvalue = {}".format(pre_1998_chisquare_value, pre_1998_pvalue))


# create a post-1998 cross tab dataframe for number of True and False Critic's Pick over the years
post_1998_crosstab_df = pd.crosstab(post_1998_df.critics_pick, post_1998_df.movie_year)

post_1998_observed, post_1998_expected, post_1998_chisquare_value, post_1998_pvalue = calculate_chisquare(post_1998_crosstab_df, post_1998_critics_pick_probability)
print("Post-1998: chi-square = {}, pvalue = {}".format(post_1998_chisquare_value, post_1998_pvalue))

pre_1998_barplot_df = create_year_factorplot_df(pre_1998_df, pre_1998_critics_pick_probability)

# Draw a nested barplot to show Critic's Pick for year and observed/expected for pre-1998 movie reviews.
pre_1998_fig = plt.figure(figsize=(14,8))

pre_1998_factorplot = sns.factorplot(x="year", y='critics_pick', data=pre_1998_barplot_df, 
                                     hue="Source", size=12, kind="bar", palette="muted")
pre_1998_factorplot.despine(left=True)
pre_1998_factorplot.set_xlabels("Year")
pre_1998_factorplot.set_ylabels("Number of Critic's Picks (Pre-1998)")
plt.show()

# save the graph 
plot_filename = 'nested_barplot_critics_pick_by_year_pre_1998.png'
plot_path = os.path.join(output_folder, plot_filename)
pre_1998_factorplot.savefig(plot_path, bbox_inches='tight')

post_1998_barplot_df = create_year_factorplot_df(post_1998_df, post_1998_critics_pick_probability)

# Draw a nested barplot to show Critic's Pick for year and observed/expected for post-1998 movie reviews.
post_1998_fig = plt.figure(figsize=(14,8))

post_1998_factorplot = sns.factorplot(x="year", y='critics_pick', data=post_1998_barplot_df, 
                                      hue="Source", size=12, kind="bar", palette="muted")
post_1998_factorplot.despine(left=True)
post_1998_factorplot.set_xlabels("Year")
post_1998_factorplot.set_ylabels("Number of Critic's Picks (Pre-1998)")
plt.show()

# save the graph 
plot_filename = 'nested_barplot_critics_pick_by_year_post_1998.png'
plot_path = os.path.join(output_folder, plot_filename)
post_1998_factorplot.savefig(plot_path, bbox_inches='tight')

# First we need to get a list of critics who have done more than 10 reviews.
counts_df = pd.DataFrame(review_df.groupby('byline').size().rename('counts'))
counts_df.sort_values(['counts'], ascending=False, inplace=True)
top_critics_temp_df = counts_df[counts_df['counts'] >= 10]
top_critics_list = list(top_critics_temp_df.index.values)

print("Top 20 critics:")
print(top_critics_list[0:20])
print("Total number of critics with 10 or more reviews:", len(top_critics_list))

# Turns out that the top critics wrote 26484 of the 26893 reviews (> 98%).
print("Reviews written by the top critics:", top_critics_temp_df['counts'].sum())

# Now we can create the usual kind of dataframe.
top_critics_df = review_df[review_df['byline'].isin(top_critics_list)]
top_critics_df.info()

# get the count for Critic's Pick 
top_cp_true = top_critics_df[top_critics_df['critics_pick'] == True]['critics_pick'].count()
top_cp_false = top_critics_df[top_critics_df['critics_pick'] == False]['critics_pick'].count()

# get probability of Critic's Pick
top_cp_probability = top_cp_true / (top_cp_true + top_cp_false)
print("Top Critic's Pick probability is: ", top_cp_probability)

# create a year cross tab dataframe for number of True and False Critic's Pick over the years
top_critics_crosstab_df = pd.crosstab(top_critics_df.critics_pick, top_critics_df.byline)

# Calculate the chi-square and p values.
top_critics_observed, top_critics_expected, top_critics_chisquare_value, top_critics_pvalue = calculate_chisquare(top_critics_crosstab_df, top_cp_probability)
print("Top critics: chi-square = {}, pvalue = {}".format(top_critics_chisquare_value, top_critics_pvalue))

review_df['mpaa_rating'].value_counts()

# create a cross tab dataframe for number of True and False Critic's Pick against MPAA ratings
ratings_crosstab_df = pd.crosstab(review_df.critics_pick, review_df.mpaa_rating)

# chi square value and p value calculation
ratings_observed, ratings_expected, ratings_chisquare_value, ratings_pvalue = calculate_chisquare(ratings_crosstab_df, 
                                                                  critics_pick_probability)
print("MPAA ratings: chi-square = {}, pvalue = {}".format(ratings_chisquare_value, ratings_pvalue))

# Rearrange the data into a format suitable for sns.factorplot().
def create_ratings_factorplot_df(df, cp_probability, verbose=False):
    nested_barplot_list = []
    for y in df['mpaa_rating'].unique():
        movie_count = df[df['mpaa_rating'] == y].shape[0]
        cp_count = df[(df['mpaa_rating'] == y) & (df['critics_pick'] == True)].shape[0]
        expected_count = movie_count * cp_probability

        if verbose:
            print("{}: {} out of {}, expected {}".format(y, cp_count, movie_count, expected_count))

        nested_barplot_list.append({'mpaa_rating':y, 'critics_pick':cp_count, 'Source':'Observed'})
        nested_barplot_list.append({'mpaa_rating':y, 'critics_pick':expected_count, 'Source':'Expected'})

    # Create a dataframe for the values, with columns [month, critics_pick, Source].
    result_df = pd.DataFrame.from_records(nested_barplot_list, columns=['mpaa_rating', 'critics_pick', 'Source'])
    result_df.sort_values('mpaa_rating', axis=0, ascending=True, inplace=True)
    result_df = result_df.reset_index(drop=True)

    return result_df

ratings_barplot_df = create_ratings_factorplot_df(review_df, critics_pick_probability)

# Draw a nested barplot to show Critic's Pick for critic and observed/expected.
ratings_fig = plt.figure(figsize=(14,8))

ratings_factorplot = sns.factorplot(x="mpaa_rating", y='critics_pick', data=ratings_barplot_df, 
                                      hue="Source", size=12, kind="bar", palette="muted")
ratings_factorplot.despine(left=True)
ratings_factorplot.set_xlabels("MPAA Rating")
ratings_factorplot.set_ylabels("Number of Critic's Picks")

plt.show()

# save the graph 
plot_filename = 'nested_barplot_critics_pick_by_mpaa_rating.png'
plot_path = os.path.join(output_folder, plot_filename)
ratings_factorplot.savefig(plot_path, bbox_inches='tight')