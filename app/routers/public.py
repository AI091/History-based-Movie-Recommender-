from fastapi import APIRouter , Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.logic.public import *
from app.schemas import *

router = APIRouter(tags=['Public'])
templates = Jinja2Templates(directory="templates")


@router.get('/',status_code = 200,response_class = HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post('/movieupdate',status_code = 200)
def movie_update(input: str):
    return {'movies' :update_movie(input)}

@router.get('/moviesearch',status_code = 200,response_class = HTMLResponse)
def movie_search(request: Request):
    return templates.TemplateResponse("moviesearch.html", {"request": request})

@router.get('/recommend',status_code = 301,response_class = HTMLResponse)
def recommend(input: str,request: Request):
    return templates.TemplateResponse("results.html", {"request": request,'data':recommend_one(input) })

@router.get('/recommends',status_code = 301,response_class = HTMLResponse)
def recommends(movie: str,request: Request):
    return templates.TemplateResponse("results.html", {"request": request,'data': recommend_three(movie.split(','))})