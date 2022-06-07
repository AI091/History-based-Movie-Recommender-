from pymongo import MongoClient

CLIENT = "mongodb://localhost:27017/"
DB = "demo"
COLLECTION = "watch"

class DatabaseHandler:
    client = MongoClient(CLIENT)
    db = client[DB]
    collection = db[COLLECTION]
    def _init_(self):

        print(self.collection)
        
    def get_collection(self):
        return self.collection.find({})

    def create(self, movie):
        if not self.collection.find_one({"title": movie["title"]}):
            self.collection.insert_one(movie)
            return movie
        else:
            return 

    def read_by_name(self, movie_name):
        try:
            return self.collection.find_one({"title": movie_name})
        except:
            print("Movie not found")
            
    def read_by_id(self, id):
        try:
            return self.collection.find_one({"_id": id})
        except:
            print("Movie not found")
            

    def read_by_letters(self, letter):
        try:
            letter = letter.title()
            return self.collection.find({"title": { "$regex": f"^{letter}" }})
        except:
            print("Movie not found")
    
