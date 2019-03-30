import json
import sys

import pymongo
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

# Checking if database already exists
my_db_name = "ImdbRottenSearch"
db_names = client.list_database_names()
if my_db_name in db_names:
    print("Database already exists..Dropping the existing database")
    try:
        client.drop_database(my_db_name)
    except IOError:
        print("Error occurred while attempting to drop database!!!")
        sys.exit()

# Create a new database for the search application
db = client['ImdbRottenSearch']
collection_names_tuple = ("movies", "movie_actors", "movie_countries", "movie_directors", "movie_genres", "movie_tags", "tags", "user_ratedmovies", "user_taggedmovies")

# Read each file and load its json data into each collection
for i in collection_names_tuple:
    # Create a new collection with names from the above array
    collection_movies = db[i]
    try:
        with open('JsonFiles/'+i+'.json', 'r', encoding="utf8") as f:
            file_data = json.load(f)
        collection_movies.insert(file_data)
        print(i+" Table inserted successfully !!!")
    except IOError:
        print("Could not read file: " + i + ".json")
        sys.exit()

# Create compound indices for the above created tables
db = client['ImdbRottenSearch']

mycol = db.movies
mycol.create_index((('id', pymongo.ASCENDING), ('title', pymongo.ASCENDING), ('year', pymongo.ASCENDING)))

mycol = db.movie_genres
mycol.create_index((('movieID', pymongo.ASCENDING), ('genre', pymongo.ASCENDING)))

mycol = db.movie_countries
mycol.create_index((('movieID', pymongo.ASCENDING), ('country', pymongo.ASCENDING)))

mycol = db.movie_actors
mycol.create_index((('movieID', pymongo.ASCENDING), ('actorName', pymongo.ASCENDING)))

mycol = db.movie_directors
mycol.create_index((('movieID', pymongo.ASCENDING), ('directorName', pymongo.ASCENDING)))

mycol = db.movie_tags
mycol.create_index((('movieID', pymongo.ASCENDING), ('tagID', pymongo.ASCENDING), ('tagWeight', pymongo.ASCENDING)))

mycol = db.tags
mycol.create_index((('id', pymongo.ASCENDING), ('value', pymongo.ASCENDING)))

mycol = db.user_taggedmovies
mycol.create_index((('userID', pymongo.ASCENDING), ('movieID', pymongo.ASCENDING), ('tagID', pymongo.ASCENDING)))

client.close()
