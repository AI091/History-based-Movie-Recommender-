import uvicorn
from app.routers import scrape
from app.routers import public
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.include_router(public.router)
app.include_router(scrape.router)
app.mount("/static", StaticFiles(directory='static'),name='static')

if __name__ == "__main__":
    uvicorn.run(app,host="127.0.0.1",port=80)

