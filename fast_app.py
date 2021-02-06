# Importing the libraries
import uvicorn
from fastapi import FastAPI
from recommender import model 

# name = input('Enter the name of the movie')

# answer = model(name)

# print(f'{answer}')

app = FastAPI()


@app.get('/')
def welcome():
	return {'message':'Welcome to a movie recommender engine'}

@app.post('/{name}')
def predict(name:str):
	answer = model(name)
	title = list(answer.Title)
	ratings = list(answer.Rating)
	count = list(answer.RatingCount)


	return {'Title:':title ,'Ratings':ratings,'No of Count':count}


if __name__=="__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)


# uvicorn fast_app:app --reload