from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from pymongo import MongoClient

def my_view(request):
    mongodb_uri = "mongodb+srv://tamilselvan:doodleblue@cluster0.2fuesru.mongodb.net/lemoneai"

    try:
        with MongoClient(mongodb_uri) as client:
            db = client['lemoneai']
            my_collection = db.list_collection_names()
            print("my_collection >>>>>>", my_collection)
            # result = my_collection.find_one({"key": "value"})
    except Exception as e:
        result = None
        
        
@login_required
def hello_world(request):
    data = {'message': 'Hello, World!'}
    return JsonResponse(data)
