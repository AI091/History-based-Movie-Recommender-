from fastapi import APIRouter
from app.schemas import *
from app.logic.scrape import ver_scrape

router = APIRouter(tags=['Scrap'])

@router.post('/scrape',status_code=201)
def scrape(pwd : str):
    ver_scrape(pwd)
