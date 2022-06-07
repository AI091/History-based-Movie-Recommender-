from app.modules.database_handler import DatabaseHandler
from app.modules.recommender import recommender

def update_movie(input:str):
    handler = DatabaseHandler()
    return [ i['title'] for i in list(handler.read_by_letters(input))[:3]]

def recommend_one(input:str):
    handler = DatabaseHandler()
    model = recommender(list(handler.get_collection()), 'features')
    model.vectorize()
    model.fit()
    model.print_count_matrix()
    model.print_sim_matrix()
    return [ handler.read_by_id(i) for i in  model.recommend(dict(handler.read_by_name(input))['_id'],6)]

def recommend_three(input:list):
    handler = DatabaseHandler()
    model = recommender(list(handler.get_collection()), 'features')
    model.vectorize()
    model.fit()
    model.print_count_matrix()
    model.print_sim_matrix()
    rec = []
    for i in input : 
        rec+=[ handler.read_by_id(x) for x in model.recommend(dict(handler.read_by_name(i))['_id'],2)]
    return rec
