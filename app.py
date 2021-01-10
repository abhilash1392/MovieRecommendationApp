from flask import Flask,request 
import numpy as np 
import pandas as pd
from flasgger import Swagger



columns=['user_id','item_id','rating','time_stamp']
df=pd.read_csv('u.data',sep='\t',names=columns)
movie_title=pd.read_csv('Movie_Id_Titles')
df=df.merge(movie_title)
df['movie_title']=df['title'].map(lambda x:(x.split(" (")[0]))
df.drop(['title'],inplace=True,axis=1)
df_rating=pd.DataFrame(df.groupby('movie_title')['rating'].mean(),columns=['rating'])
df_rating['rating_count']=df.groupby('movie_title')['rating'].count()
moviemat=df.pivot_table(index='user_id',columns='movie_title',values='rating')

def get_recommended_movies(name):
    if name not in list(df.movie_title):
        return 'Sorry, this movie is not in our database!'
    else:
        movie_name_user_ratings=moviemat[name]
        similar_to_movie_name=moviemat.corrwith(movie_name_user_ratings)
        corr_movie=pd.DataFrame(similar_to_movie_name,columns=['Correlation'])
        corr_movie.dropna(inplace=True)
        corr_movie=corr_movie.join(df_rating['rating_count'])
        recommended_movies=corr_movie[corr_movie['rating_count']>100].sort_values('Correlation',ascending=False).head(6)
        recommended_movies.reset_index(inplace=True)
        
        return list(recommended_movies.movie_title)


app=Flask(__name__)
Swagger(app)

@app.route('/')
def welcome():
	return 'Welcome All'

@app.route('/recommend',methods=['Get'])
def recommendation():

    """ Let's recommend movies
    This is using docstrings for specifications.
    ---
    parameters:
      - name: name
        in: query
        type: string
        required: true
        
    responses:
        200:
            description: The output values is 

    """ 
    
    name=request.args.get("name")
    movies=get_recommended_movies(name)
    return str(movies)
	






if __name__=="__main__":
	app.run()