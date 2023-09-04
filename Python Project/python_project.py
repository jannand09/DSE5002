# -*- coding: utf-8 -*-
"""
You are a data scientist and would like to know where the top 5 places in the 
world (country or city) where your salary will go the farthest with respect to 
each individual index within the cost_of_living.csv file. Provide a simple 
statistical analysis in a Jupyter Notebook file and provide visualizations 
to support your analysis (I am looking for data wrangling more than anything). 
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

cost_of_living_data = pd.read_csv("cost_of_living.csv")
ds_salaries = pd.read_csv("ds_salaries.csv")
levels_fyi_salary_data = pd.read_csv("Levels_Fyi_Salary_Data.csv")
country_codes_data = pd.read_excel("country_codes.xlsx")


levels_fyi_data = pd.DataFrame(levels_fyi_salary_data.loc[levels_fyi_salary_data['title'].str.contains("(D|d)ata"), :])
new = levels_fyi_data["location"].str.split(", ", n = -1, expand = True)
levels_fyi_data['city'] = new[0]
levels_fyi_data['state.or.province'] = new[1]
levels_fyi_data['country'] = new[2]
levels_fyi_data.rename(columns={'title': 'job_title', 'totalyearlycompensation': 'salary_in_usd'}, inplace=True)
levels_fyi_data.reset_index(inplace=True)
for i in range(len(levels_fyi_data)):
    if pd.isnull(levels_fyi_data.at[i, 'country']):
        levels_fyi_data.loc[i, 'country'] = "United States"

levels_fyi_data.at[0, 'country']

us_code_index = country_codes_data.index[country_codes_data['Alpha-2 code'] == "US"].tolist()
country_codes_data.loc[us_code_index[0], 'Country'] = "United States"

ds_salaries.rename(columns={'company_location': 'country'}, inplace=True)
for i in range(len(ds_salaries)):
    code = ds_salaries.at[i, 'country']
    conversion = pd.DataFrame(country_codes_data.loc[country_codes_data['Alpha-2 code'] == code, 'Country']).iat[0,0]
    ds_salaries.loc[i, 'country'] = conversion

cost_of_living_data.rename(columns={'City': 'location'}, inplace=True)
new = cost_of_living_data['location'].str.split(", ", n=-1, expand=True)
cost_of_living_data['city'] = new[0]
cost_of_living_data['state.or.province'] = new[1]
cost_of_living_data['country'] = new[2]
for i in range(len(cost_of_living_data)):
    if pd.isnull(cost_of_living_data.at[i, 'country']):
        cost_of_living_data.loc[i, 'country'] = cost_of_living_data.at[i, 'state.or.province']

all_salaries_df = pd.merge(levels_fyi_data, 
                           ds_salaries, 
                           how='outer')
cleaned_salary = all_salaries_df.loc[:, 
                                    ['job_title', 'salary_in_usd', 'city', 'state.or.province', 'country']]

city_median_df = pd.DataFrame(cleaned_salary.groupby(by="city")['salary_in_usd'].median())
city_median_df.reset_index(inplace=True)

city_rankings_df = pd.merge(city_median_df, 
                            cost_of_living_data, 
                            how='outer')
city_rankings_df = city_rankings_df.assign(cost_rating = lambda x: city_rankings_df['salary_in_usd'] / city_rankings_df['Cost of Living Index'],
                                          rent_rating = lambda x: city_rankings_df['salary_in_usd'] / city_rankings_df['Rent Index'],
                                          living_rent_rating = lambda x: city_rankings_df['salary_in_usd'] / city_rankings_df['Cost of Living Plus Rent Index'],
                                          groceries_rating = lambda x: city_rankings_df['salary_in_usd'] / city_rankings_df['Groceries Index'],
                                          restaurant_rating = lambda x: city_rankings_df['salary_in_usd'] / city_rankings_df['Restaurant Price Index'],
                                          purchase_rating = lambda x: city_rankings_df['salary_in_usd'] / city_rankings_df['Local Purchasing Power Index'])

cost = city_rankings_df.sort_values(by=['cost_rating'], ascending=False).reset_index().loc[0:4, ['city', 'cost_rating']]
sns.barplot(data=cost, x='city', y='cost_rating')
plt.xlabel("City")
plt.ylabel("Top 5 Cities in Cost of Living Rating")

rent = city_rankings_df.sort_values(by=['rent_rating'], ascending=False).reset_index().loc[0:4, ['city', 'rent_rating']]
sns.barplot(data=rent, x='city', y='rent_rating')
plt.xlabel("City")
plt.ylabel("Top 5 Cities in Cost of Rent Rating")

living_rent = city_rankings_df.sort_values(by=['living_rent_rating'], ascending=False).reset_index().loc[0:4, ['city', 'living_rent_rating']]
sns.barplot(data=living_rent, x='city', y='living_rent_rating')
plt.xlabel("City")
plt.ylabel("Top 5 Cities in Cost of Living and Rent Rating")

groceries = city_rankings_df.sort_values(by=['groceries_rating'], ascending=False).reset_index().loc[0:4, ['city', 'groceries_rating']]
sns.barplot(data=groceries, x='city', y='groceries_rating')
plt.xlabel("City")
plt.ylabel("Top 5 Cities in Cost of Groceries Rating")

restaurant = city_rankings_df.sort_values(by=['restaurant_rating'], ascending=False).reset_index().loc[0:4, ['city', 'restaurant_rating']]
sns.barplot(data=restaurant, x='city', y='restaurant_rating')
plt.xlabel("City")
plt.ylabel("Top 5 Cities in Restaurant Prices Rating")

purchase = city_rankings_df.sort_values(by=['purchase_rating'], ascending=False).reset_index().loc[0:4, ['city', 'purchase_rating']]
sns.barplot(data=purchase, x='city', y='purchase_rating')
plt.xlabel("City")
plt.ylabel("Top 5 Cities in Purchasing Power Rating")


country_median_df = pd.DataFrame(cleaned_salary.groupby(by="country")['salary_in_usd'].median())
country_median_df.reset_index(inplace=True)
cost_country_group = pd.DataFrame(cost_of_living_data.groupby(by="country").agg('median'))
cost_country_group.reset_index(inplace=True)

country_rankings_df = pd.merge(country_median_df, 
                            cost_country_group, 
                            how='outer')
country_rankings_df = country_rankings_df.assign(cost_rating = lambda x: country_rankings_df['salary_in_usd'] / country_rankings_df['Cost of Living Index'],
                                          rent_rating = lambda x: country_rankings_df['salary_in_usd'] / country_rankings_df['Rent Index'],
                                          living_rent_rating = lambda x: country_rankings_df['salary_in_usd'] / country_rankings_df['Cost of Living Plus Rent Index'],
                                          groceries_rating = lambda x: country_rankings_df['salary_in_usd'] / country_rankings_df['Groceries Index'],
                                          restaurant_rating = lambda x: country_rankings_df['salary_in_usd'] / country_rankings_df['Restaurant Price Index'],
                                          purchase_rating = lambda x: country_rankings_df['salary_in_usd'] / country_rankings_df['Local Purchasing Power Index'])

cost = country_rankings_df.sort_values(by=['cost_rating'], ascending=False).reset_index().loc[0:4, ['country', 'cost_rating']]
sns.barplot(data=cost, x='country', y='cost_rating')
plt.xlabel("country")
plt.ylabel("Cost of Living Rating")
plt.title("Top 5 Countries in Cost of Living Rating")

rent = country_rankings_df.sort_values(by=['rent_rating'], ascending=False).reset_index().loc[0:4, ['country', 'rent_rating']]
sns.barplot(data=rent, x='country', y='rent_rating')
plt.xlabel("country")
plt.ylabel("Cost of Rent Rating")
plt.title("Top 5 Countries in Cost of Rent Rating")

living_rent = country_rankings_df.sort_values(by=['living_rent_rating'], ascending=False).reset_index().loc[0:4, ['country', 'living_rent_rating']]
sns.barplot(data=living_rent, x='country', y='living_rent_rating')
plt.xlabel("country")
plt.ylabel("Cost of Living and Rent Rating")
plt.title("Top 5 Countries in Cost of Living and Rent Rating")

groceries = country_rankings_df.sort_values(by=['groceries_rating'], ascending=False).reset_index().loc[0:4, ['country', 'groceries_rating']]
sns.barplot(data=groceries, x='country', y='groceries_rating')
plt.xlabel("country")
plt.ylabel("Cost of Groceries Rating")
plt.title("Top 5 Countries in Cost of Groceries Rating")

restaurant = country_rankings_df.sort_values(by=['restaurant_rating'], ascending=False).reset_index().loc[0:4, ['country', 'restaurant_rating']]
sns.barplot(data=restaurant, x='country', y='restaurant_rating')
plt.xlabel("country")
plt.ylabel("Restaurant Prices Ratings")
plt.title("Top 5 Countries in Restaurant Prices Rating")

purchase = country_rankings_df.sort_values(by=['purchase_rating'], ascending=False).reset_index().loc[0:4, ['country', 'purchase_rating']]
sns.barplot(data=purchase, x='country', y='purchase_rating')
plt.xlabel("country")
plt.ylabel("Purchasing Power Rating")
plt.title("Top 5 Countries in Purchasing Power Rating")