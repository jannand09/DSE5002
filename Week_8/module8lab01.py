# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 12:33:05 2023

@author: jannand
"""
# Import Libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import chain

# Question 1
titles_data = pd.read_csv("Data/Netflix/titles.csv")
credits_data = pd.read_csv("Data/Netflix/credits.csv")

genres = list(titles_data['genres'].unique())

for i in range(len(genres)):
    genres[i] = genres[i].replace("[", "").replace("]", "").replace(",", "").replace("'", "")
    genres[i] = genres[i].split()

genres = list(chain.from_iterable(genres))
genres = pd.Series(genres).unique()
print(genres.size)


# Question 2

movies = titles_data[titles_data['type'] == "MOVIE"]

movies_year = movies.groupby(by="release_year")['imdb_score'].max()

highest_rated = pd.DataFrame(movies_year)

print(highest_rated.idxmax())

# Question 3

acting_credits = pd.DataFrame(credits_data.groupby(by='id')['name'].count())
movie_id = acting_credits['name'].idxmax()
print(pd.DataFrame(titles_data.loc[titles_data['id'] == movie_id, 'title']))

# Question 4

de_niro_credits = pd.DataFrame(credits_data.loc[credits_data['name'] == "Robert De Niro", 'id'])

de_niro_id = list(de_niro_credits['id'])

de_niro_movies = pd.DataFrame(titles_data.loc[titles_data['id'].isin(de_niro_id), :])

print(de_niro_movies.at[de_niro_movies['imdb_score'].idxmax(), 'title'])
print(de_niro_movies.at[de_niro_movies['imdb_score'].idxmax(), 'release_year'])

sns.kdeplot(data=de_niro_movies, x="imdb_score")

# Question 5

titles_data['war_movies'] = np.where(titles_data['description'].str.contains("war"), True, False)
titles_data['gangster_movies'] = np.where(titles_data['description'].str.contains("gangster"), True, False)

print(len(titles_data[titles_data['war_movies'] == True]))
print(len(titles_data[titles_data['ganster_movies'] == True]))

war_movie_data = titles_data.loc[titles_data['war_movies'] == True, :]
gang_movie_data = titles_data.loc[titles_data['gangster_movies'] == True, :]

war_score = np.mean(war_movie_data['imdb_score'])
gangster_score = np.mean(gang_movie_data['imdb_score'])
if  (war_score > gangster_score):
    print(f"Average war movie IMdB score of {war_score} is higher than average gangster movie score of {gangster_score}")
else:
    print(f"Average ganster movie IMdB score of {gangster_score} is higher than average war movie score of {war_score}")

sns.kdeplot(data=war_movie_data, x='imdb_score')
sns.kdeplot(data=gangster_score, x='imdb_score')