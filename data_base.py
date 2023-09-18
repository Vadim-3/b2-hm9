import pymongo
import json

client = pymongo.MongoClient("mongodb+srv://bezhukvadim56:VVBXIIBVTdILQpyb@cluster0.ssxsfik.mongodb.net/?retryWrites=true&w=majority")
db = client["mydatabase"]

with open('quotes.json', 'r', encoding='utf-8') as quotes_file:
    quotes_data = json.load(quotes_file)

with open('authors.json', 'r', encoding='utf-8') as authors_file:
    authors_data = json.load(authors_file)

quotes_collection = db["quotes"]
quotes_collection.insert_many(quotes_data)

authors_collection = db["authors"]
authors_collection.insert_many(authors_data)
