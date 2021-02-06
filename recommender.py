#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 13:26:12 2021

@author: abhilash
"""
# Importing the libraries
import pandas as pd
import numpy as np 
import re 



def model(name):
    # Loading the files in dataframe
    
    df = pd.read_csv('u.data',names=['user_id','item_id','ratings','timestamp'],delimiter='\t')
    movie_name = pd.read_csv('Movie_Id_Titles')
    # Data Cleaning
    
    movie_name['title']= movie_name['title'].apply(lambda x: cleaning_data(x))
    # Merging dataframes df and movie_name 
    
    df = df.merge(movie_name)
    # Dropping unwanted columns
    
    df.drop(['item_id','timestamp'],axis=1,inplace=True)
    # Creating a new ratings dataframe which will group ratings and rating counts
    
    df_rating = pd.DataFrame(df.groupby('title')['ratings'].mean(),columns=['ratings'])
    df_rating['rating_count'] = df.groupby('title')['ratings'].count()

    # Pivoting the data table
    moviemat = df.pivot_table(index='user_id',columns='title',values='ratings',aggfunc=np.mean)
    
    # getting the rating from moviemat 
    movie_user_name_rating = moviemat[name]
    # getting names and correlation
    similar_to_movie_ratings = moviemat.corrwith(movie_user_name_rating)
    # creating the answer dataframe, joining it with df_ratings and getting top ratings
    answer = pd.DataFrame(similar_to_movie_ratings,columns=['Correlation'])
    answer = answer.join(df_rating)
    answer = answer[answer['rating_count']>100].sort_values('Correlation',ascending=False).head(6)
    answer = answer.reset_index()
    answer.columns = ['Title','Correlation','Rating','RatingCount']
    answer.drop('Correlation',axis=1,inplace=True)
    # Returning the result
    answer.drop([0],axis=0,inplace=True)
    return answer

def cleaning_data(x):
    x=x[:-7]
    return x