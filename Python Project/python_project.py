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

ds_salaries.rename(columns={'company_location': 'country'}, inplace=True)

cost_of_living_data.rename(columns={'City': 'location'}, inplace=True)
new = cost_of_living_data['location'].str.split(", ", n=-1, expand=True)
cost_of_living_data['city'] = new[0]
cost_of_living_data['state.or.province'] = new[1]
cost_of_living_data['country'] = new[2]


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
print(city_rankings_df.columns)
city_rankings_df = city_rankings_df.assign(cost_rating = lambda x: city_rankings_df['salary_in_usd'] / city_rankings_df['Cost of Living Index'],
                                          rent_rating = lambda x: city_rankings_df['salary_in_usd'] / city_rankings_df['Rent Index'],
                                          living_rent_rating = lambda x: city_rankings_df['salary_in_usd'] / city_rankings_df['Cost of Living Plus Rent Index'],
                                          groceries_rating = lambda x: city_rankings_df['salary_in_usd'] / city_rankings_df['Groceries Index'],
                                          restaurant_rating = lambda x: city_rankings_df['salary_in_usd'] / city_rankings_df['Restaurant Price Index'],
                                          purchase_rating = lambda x: city_rankings_df['salary_in_usd'] / city_rankings_df['Local Purchasing Power Index'])

cost = city_rankings_df.sort_values(by=['cost_rating'], ascending=False).reset_index().loc[0:4, ['city', 'cost_rating']]
sns.barplot(data=cost, x='city', y='cost_rating')
plt.xlabel("City")
plt.ylabel("Cost of Living Rating")

rent = city_rankings_df.sort_values(by=['rent_rating'], ascending=False).reset_index().loc[0:4, ['city', 'rent_rating']]
sns.barplot(data=rent, x='city', y='rent_rating')
plt.xlabel("City")
plt.ylabel("Cost of Rent Rating")

living_rent = city_rankings_df.sort_values(by=['living_rent_rating'], ascending=False).reset_index().loc[0:4, ['city', 'living_rent_rating']]
sns.barplot(data=living_rent, x='city', y='living_rent_rating')
plt.xlabel("City")
plt.ylabel("Cost of Living and Rent Rating")

groceries = city_rankings_df.sort_values(by=['groceries_rating'], ascending=False).reset_index().loc[0:4, ['city', 'groceries_rating']]
sns.barplot(data=groceries, x='city', y='groceries_rating')
plt.xlabel("City")
plt.ylabel("Cost of Groceries Rating")

restaurant = city_rankings_df.sort_values(by=['restaurant_rating'], ascending=False).reset_index().loc[0:4, ['city', 'restaurant_rating']]
sns.barplot(data=restaurant, x='city', y='restaurant_rating')
plt.xlabel("City")
plt.ylabel("Restaurant Prices Rating")

purchase = city_rankings_df.sort_values(by=['purchase_rating'], ascending=False).reset_index().loc[0:4, ['city', 'purchase_rating']]
sns.barplot(data=purchase, x='city', y='purchase_rating')
plt.xlabel("City")
plt.ylabel("Purchasing Power Rating")

