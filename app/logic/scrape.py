from app.modules.scraper import MovieScrap
from app.modules.database_handler import DatabaseHandler
from app.modules.cleaner import clean
from fastapi import HTTPException,status
from hashlib import sha256


def ver_scrape(pwd: str):
    pwd = str.encode(pwd)
    if sha256(pwd).hexdigest() == "614b50aa05247f1afaad1512ee19034bd16cd348b3d35a0c548cec37e9b896da":
        scraper = MovieScrap(14,6)
        handler = DatabaseHandler()
        movies = scraper.scrape()
        cleaner = clean(movies)
        cleaner.run()
        movies = cleaner.save_to_dict()
        for movie in movies:
            handler.create(movie)
    else :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Verification Failed ")
