from fastapi import FastAPI , HTTPException , Request
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import joblib
import numpy as np

app = FastAPI()

model = joblib.load('final_model.joblib')

# Подключение статических файлов (CSS, JS)
app.mount('/static' , StaticFiles(directory="static") , name = "static")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "flowers": flowers_db})


templates = Jinja2Templates(directory="templates")

class Flower(BaseModel):
	sepal_length:float
	sepal_width:float
	petal_length:float
	petal_width:float

flowers_db = []

@app.delete('/delete_flower/{index}')
def delete_flower(index : int ):
	if index < 0 or index >= len(flowers_db):
		raise HTTPException(status_code = 404 , detail = "Flower not found")
	deleted_flower = flowers_db.pop(index)
	return {'data' : 'Flower is deleted' , 'deleted flower' : deleted_flower}

@app.put('/update_flower/{index}')
def update_flower(index:int , flower : Flower):
	if index < 0 or index >= len(flowers_db):
		raise HTTPException(status_code = 404 , detail = "Flower not found")
	flowers_db[index] = flower
	return {'data' : f'Flower at {index} position is updated'}

@app.post('/flowers')
def add_flower(flower : Flower):
	if flower.petal_length <= 0.0 or flower.petal_width <= 0.0 or flower.sepal_length <= 0.0 or flower.sepal_width <= 0.0:
		raise HTTPException(status_code=404 , detail = "It is not possible")
	flowers_db.append(flower)
	return {'data' : 'Flower is added' , 'flower' : flower}

@app.get('/get_flowers/{index}')
def get_flowers(index:int):
	if index < 0 or index >= len(flowers_db):
		raise HTTPException(status_code=404 , detail = "Flower not found")
	return {'data' : flowers_db[index]}

@app.post('/predict_flower')
def predict_flower(flower : Flower):
	features = np.array([[flower.sepal_length , flower.sepal_width , flower.petal_length , flower.petal_width]])
	predict = model.predict(features)

	flower_map = {0 : "setosa" , 1 : "versicolor" , 2 : "virginica"}

	return {'data' : f'Predict is {flower_map[predict[0]]}'}
