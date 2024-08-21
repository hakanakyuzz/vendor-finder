# insert documents into a new collections from collections that already exist

# from pymongo import MongoClient
# import certifi
# from bson import ObjectId
# from config import MONGO_URI

# # Establish MongoDB connection
# client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
# db = client['vendors']

# # Check connection
# client.admin.command('ping')
# print("MongoDB connection successful.")

# # List of old collections to merge
# old_collections = ['213f0e2d', 'd16cc483', 'e5fcc923', 'f8ae52c9']

# # New collection name
# new_collection_name = "theWholeSalerTes_3"
# new_collection = db[new_collection_name]

# # Iterate over each old collection and insert documents into the new collection
# for collection_name in old_collections:
#     old_collection = db[collection_name]
#     documents = old_collection.find()
#     for document in documents:
#         document['_id'] = ObjectId()  # Generate a new unique ObjectId
#         new_collection.insert_one(document)

# print("Documents merged successfully into the collection:", new_collection_name)


#############


# checks by query to find same

# from pymongo import MongoClient
# import certifi
# from bson import ObjectId
# from urllib.parse import urlparse
# from config import MONGO_URI

# # Function to extract the base URL
# def get_base_url(url):
#     parsed_url = urlparse(url)
#     return f"{parsed_url.scheme}://{parsed_url.netloc}"

# # Establish MongoDB connection
# client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
# db = client['vendors']

# # Check connection
# client.admin.command('ping')
# print("MongoDB connection successful.")

# # List of old collections to merge
# old_collections = ['213f0e2d', 'd16cc483', 'e5fcc923', 'f8ae52c9']

# # New collection name
# new_collection_name = "theWholeSalerTest_5"
# new_collection = db[new_collection_name]

# # Set to track unique query values
# unique_queries = set()

# # Iterate over each old collection and insert documents into the new collection
# for collection_name in old_collections:
#     old_collection = db[collection_name]
#     documents = old_collection.find()
#     for document in documents:
#         # Modify the query field to only contain the base URL
#         if 'query' in document:
#             base_url = get_base_url(document['query'])
#             if base_url in unique_queries:
#                 continue  # Skip if this query already exists
#             unique_queries.add(base_url)
#             document['query'] = base_url

#         # Generate a new unique ObjectId
#         document['_id'] = ObjectId()

#         new_collection.insert_one(document)

# print("Documents merged successfully into the collection:", new_collection_name)


#############


# checks by mail to find same

# from pymongo import MongoClient
# import certifi
# from bson import ObjectId
# from urllib.parse import urlparse
# from config import MONGO_URI

# # Function to extract the base URL
# def get_base_url(url):
#     parsed_url = urlparse(url)
#     return f"{parsed_url.scheme}://{parsed_url.netloc}"

# # Establish MongoDB connection
# client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
# db = client['vendors']

# # Check connection
# client.admin.command('ping')
# print("MongoDB connection successful.")

# # List of old collections to merge
# old_collections = ['213f0e2d', 'd16cc483', 'e5fcc923', 'f8ae52c9']

# # New collection name
# new_collection_name = "theWholeSalerTest_6"
# new_collection = db[new_collection_name]

# # Set to track unique email values
# unique_emails = set()

# # Iterate over each old collection and insert documents into the new collection
# for collection_name in old_collections:
#     old_collection = db[collection_name]
#     documents = old_collection.find()
#     for document in documents:
#         # Modify the query field to only contain the base URL
#         if 'query' in document:
#             document['query'] = get_base_url(document['query'])

#         # Check for unique emails
#         emails = [email['value'] for email in document.get('emails', [])]
#         if any(email in unique_emails for email in emails):
#             continue  # Skip if any email in this document is already encountered
#         unique_emails.update(emails)

#         # Generate a new unique ObjectId
#         document['_id'] = ObjectId()

#         new_collection.insert_one(document)

# print("Documents merged successfully into the collection:", new_collection_name)


#############


# ai working test
# from utils import classify_text
# from config import categories


# sample_text = "This is a sample description of a vendor providing sound and show services for events."
# print(classify_text(sample_text, categories))


#############


# classify and give weight tho ones who already didnt

# from utils import classify_text, calculate_weight
# from config import categories
# from db import connect_to_mongo
#
#
# def process_documents():
#     db = connect_to_mongo()
#     if db is None:
#         return
#
#     source_collection = db["theWholeSalerTest_5"]
#     target_collection = db["theWholeSalerTest_6"]
#
#     documents = source_collection.find({"site_data.description": {"$exists": True, "$ne": ""}})
#
#     for doc in documents:
#         description = doc["site_data"]["description"]
#         classification, score = classify_text(description, categories)
#
#         # Skip documents without a confident classification
#         if classification == "No confident classification result." or classification is None:
#             print(f"Skipping document with _id: {doc['_id']} due to no confident classification")
#             continue
#
#         doc["classification"] = {'category': classification, 'score': score}
#         doc["weight"] = calculate_weight(doc)
#
#         target_collection.insert_one(doc)
#         print(f"Inserted document with _id: {doc['_id']} into the new collection")
#
#
# process_documents()


#############


# create a data collection in mongo from collections already exist, check if there is any duplicate by looking query

from db import connect_to_mongo
from excel import create_excel_file


def merge_collections():
    db = connect_to_mongo()
    if db is None:
        return

    collection_names = [name for name in db.list_collection_names() if name != 'data']

    all_data = []
    seen_queries = set()
    for collection_name in collection_names:
        collection = db[collection_name]
        for item in collection.find({}):
            if item['query'] not in seen_queries:
                seen_queries.add(item['query'])
                all_data.append(item)

    db['data'].drop()

    new_collection = db['data']
    if all_data:
        new_collection.insert_many(all_data)

    print("Data merged and duplicates removed based on 'query'. New collection 'data' created.")
    create_excel_file('data')


merge_collections()


#############


# console javascript function

# function getElementsByClassName(className) {
# return document.getElementsByClassName(className)
# }
#
# console.log(getElementsByClassName('class'))