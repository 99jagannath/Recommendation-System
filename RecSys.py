# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 23:25:46 2020

@author: Bibhupad
"""

import pandas as pd 
import numpy as np
import warnings
warnings.filterwarnings('ignore')

#The dataset is tab separated so we pass in \t to the sep parameter. 
#We then pass in the column names using the names parameter.
df = pd.read_csv('ratings.dat', sep='::', names=['user_id','item_id','rating','titmestamp'])
df.head()

movie_titles = pd.read_csv('movies.dat',sep='::',names=['user_id','title','genre'])
movie_titles.head()

df = pd.merge(df, movie_titles, on='user_id')
df.head()

#Using the describe or info commands we can get a brief description of our dataset. 
#This is important in order to enable us understand the dataset we are working with.
df.describe()

#we shall use the Pearson correlation coefficient. 
#This number will lie between -1 and 1. 
#1 indicates a positive linear correlation while -1 indicates a negative correlation.
# 0 indicates no linear correlation. Therefore movies with a zero correlation are not similar at all.
# In order to create this dataframe we use pandas groupby functionality.
# We group the dataset by the title column and compute its mean to obtain the average rating for each movie.

# a dataframe with the average rating for each movie and the number of ratings
ratings = pd.DataFrame(df.groupby('title')['rating'].mean())
ratings.head()


ratings['number_of_ratings'] = df.groupby('title')['rating'].count()
ratings.head()

#plot a Histogram using pandas plotting functionality to visualize the distribution of the ratings
import matplotlib.pyplot as plt
ratings['rating'].hist(bins=50)

#check the relationship between the rating of a movie and the number of ratings.
import seaborn as sns
sns.jointplot(x='rating', y='number_of_ratings', data=ratings)

movie_matrix = df.pivot_table(index='item_id', columns='title')
movie_matrix.head()

#the user has watched toy story and Jumanji. Find similar movie
toy_story_user_rating = movie_matrix['rating','Toy Story (1995)']
jumanji_user_rating = movie_matrix['rating','Jumanji (1995)']


#Compute the correlation between two dataframes we use pandas corwith functionality.
#Corrwith computes the pairwise correlation of rows or columns of two dataframe objects
similar_to_jumanji=movie_matrix.corrwith(jumanji_user_rating)
similar_to_jumanji.head()

similar_to_toy_story=movie_matrix.corrwith(toy_story_user_rating)
similar_to_toy_story

corr_jumanji = pd.DataFrame(similar_to_jumanji, columns=['Correlation'])
corr_jumanji.dropna(inplace=True)
corr_jumanji.head()

corr_toy_story = pd.DataFrame(similar_to_toy_story, columns=['Correlation'])
corr_toy_story.dropna(inplace=True)
corr_toy_story.head()

corr_toy_story = corr_toy_story.join(ratings['number_of_ratings'])
corr_jumanji = corr_jumanji.join(ratings['number_of_ratings'])
corr_toy_story .head()
corr_jumanji.head()

corr_toy_story[corr_toy_story['number_of_ratings'] > 100].sort_values(by='Correlation', ascending=False).head(10)
corr_jumanji[corr_jumanji['number_of_ratings'] > 100].sort_values(by='Correlation', ascending=False).head(10)