import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Importing data
rawdata = pd.read_csv(r"C:\Users\YunusEmreÖzen\Desktop\Datasets\Global YouTube Statistics.csv", encoding='ANSI')

#Looking into basic structure and properties of data
rawdata.info()

#We look into data and replace index with rank
rawdata.set_index(["rank"], inplace = True)

#Since category and channel_type are nearly same datas, we will drop channel_type column
rawdata.drop(["channel_type"], axis = 1)


# We should transform to created year , month, day to single date

#First we should replace months as numbers
clean_data = rawdata.replace(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],[1,2,3,4,5,6,7,8,9,10,11,12])

#Notice that we have some nonsense data says that 1970, We know that, Youtube established in 2005 so we should drop that.
clean_data = clean_data[clean_data["created_year"] >= 2005]

#Convert year data to int, so we can get cleaner data
clean_data["created_year"] = clean_data["created_year"].astype(int)

#Then we can plot datas according to years
#sns.countplot(y = clean_data["created_year"])

# Then we can see how many channels created in YouTube for each year                            

#Let us do some other basic plot to see basic properties of data

#We would see top 10 countries on each country
sns.countplot(y = clean_data["Country"],  order=pd.value_counts(clean_data["Country"]).iloc[:10].index)

#by using same methods we can examine how many channel category etc. 



# I want to examine lowest and highest earning per year of channels by country by plotting multiple bar plot that consisting lowest and highest earning per year. Since youtube income depends on country that may give us precise insight. Also we may examine according to category to understand better.

# Filter out countries that occur less than 5 times
country_counts = clean_data['Country'].value_counts()
valid_countries = country_counts[country_counts >= 5].index
filtered_clean_data = clean_data[clean_data['Country'].isin(valid_countries)]


highest_average_earnings_per_country = filtered_clean_data.groupby('Country')['highest_yearly_earnings'].mean().reset_index()
high_top_10_countries = highest_average_earnings_per_country.nlargest(10, 'highest_yearly_earnings')
high_top_10_countries.set_index(["Country"], inplace = True)

#sns.barplot(y='Country', x='highest_yearly_earnings', data = high_top_10_countries)
                  

lowest_average_earnings_per_country = filtered_clean_data.groupby('Country')['lowest_yearly_earnings'].mean().reset_index()
low_top_10_countries = lowest_average_earnings_per_country.nlargest(10, 'lowest_yearly_earnings')
low_top_10_countries.set_index(["Country"], inplace = True)

df = pd.merge(low_top_10_countries, high_top_10_countries,left_index=True, right_index=True)

# Create a horizontal bar plot
df.plot(kind='barh', figsize=(10, 6))
plt.title('Lowest and Highest Yearly Earnings by Country')
plt.xlabel('Earnings')
plt.ylabel('Country')
plt.tight_layout()

# Show the plot
plt.show()




category_counts = clean_data['category'].value_counts()
valid_Categories = category_counts[category_counts >= 5].index
filtered_clean_data = clean_data[clean_data['category'].isin(valid_Categories)]


highest_average_earnings_per_category = filtered_clean_data.groupby('category')['highest_yearly_earnings'].mean().reset_index()
high_top_10_Categories = highest_average_earnings_per_category.nlargest(10, 'highest_yearly_earnings')
high_top_10_Categories.set_index(["category"], inplace = True)

#sns.barplot(y='category', x='highest_yearly_earnings', data = high_top_10_Categories)
                  

lowest_average_earnings_per_category = filtered_clean_data.groupby('category')['lowest_yearly_earnings'].mean().reset_index()
low_top_10_Categories = lowest_average_earnings_per_category.nlargest(10, 'lowest_yearly_earnings')
low_top_10_Categories.set_index(["category"], inplace = True)

df = pd.merge(low_top_10_Categories, high_top_10_Categories,left_index=True, right_index=True)

# Create a horizontal bar plot
df.plot(kind='barh', figsize=(10, 6))
plt.title('Lowest and Highest Yearly Earnings by category')
plt.xlabel('Earnings')
plt.ylabel('category')
plt.tight_layout()

# Show the plot
plt.show()


#Note that it is remarkable such that even though United States are on the top 10, the average earning is on the 10th. I think it might be because of there are too many channel on USA.

#Then I want to see the correlation betweens of viewers and earnings and compare them.I think if we look the earnings per view we may get more informative data. Although, we have last month view, we dont have earning for each month. So we should make predictions on these datas.

clean_data["highest_earning_per_view_monthly"] = clean_data["highest_yearly_earnings"] / clean_data["video_views_for_the_last_30_days"]


country_counts = clean_data['Country'].value_counts()
valid_countries = country_counts[country_counts >= 5].index
filtered_clean_data = clean_data[clean_data['Country'].isin(valid_countries)]


highest_average_earnings_per_country = filtered_clean_data.groupby('Country')['highest_earning_per_view_monthly'].mean().reset_index()
high_top_10_countries_monthly = highest_average_earnings_per_country.nlargest(10, 'highest_earning_per_view_monthly')
high_top_10_countries_monthly.set_index(["Country"], inplace = True)


high_top_10_countries_monthly.plot(kind = "barh", figsize = (10,6))
plt.show()

#My last goal is analyzing how it affect to subscriber count to views. I use correlation method to examine it.

corr = clean_data["subscribers_for_last_30_days"].corr(clean_data["video_views_for_the_last_30_days"])

#Although it seems subscriptions may affect views, it does not affect that much. We should examine reasons better.
