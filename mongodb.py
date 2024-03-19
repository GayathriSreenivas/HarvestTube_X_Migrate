from pymongo import MongoClient

mongo_uri = "mongodb://localhost:27017/"
client = MongoClient(mongo_uri)

database_list = client.list_database_names()
print("List of databases:")
for db in database_list:
    print(db)

data = {"channel_name" : "Mashmool" , "channel_description" : "Vampire Teeth"}

database_name = "youtube"
collect = client[database_name]

collection_names = collect.list_collection_names()
channel_collection = collect[collection_names[0]]

result = channel_collection.insert_one(data)
print(result)
client.close()


