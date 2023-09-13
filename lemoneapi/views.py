from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from pymongo import MongoClient
import uuid
from . models import Users
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import os
from datetime import datetime, timedelta
from django.conf import settings
import bcrypt
from bson import json_util
import jwt
import json
import math

from .decorators import verify_token
client = MongoClient(settings.DATABASE_URL)
db = client[settings.DATABASE_NAME]
users = db['users']
inventory = db['inventory_info']

def index(request):
    return HttpResponse("Hi this is doodbleblue")

@csrf_exempt
def register(request):
    try:
        if request.method == 'POST':
            data = request.POST
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            if all((username, email, password)):
                if users.find_one({"username": username}):
                    return JsonResponse({"message": "Username already exists", "status": 400}, status=400)

                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                user_data = {
                    'user_id': str(uuid.uuid4()),
                    "username": username,
                    "email": email,
                    "password": hashed_password.decode('utf-8'),
                    "createdAt": datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                }
                users.insert_one(user_data)
                return JsonResponse({"message": "Registration successful", "status": 200}, status=200)
            else:
                return JsonResponse({"message": "Missing data in the request", "status": 400}, status=400)
        else:
            return JsonResponse({"message": "Method not allowed", "status": 405}, status=405)

    except Exception as e:
        return JsonResponse({"message": "An error occurred", "status": 500}, status=500)


@verify_token
def hello_world(request):
    data = {'message': 'Hello, World!'}
    return JsonResponse(data)


@csrf_exempt
def login(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            username = data.get('username')
            password = data.get('password')
            if username and password:
                user_data = users.find_one({"username": username})
                if user_data and bcrypt.checkpw(password.encode('utf-8'), user_data['password'].encode('utf-8')):
                    token = jwt.encode({'user_id': user_data['user_id'], 'exp': datetime.utcnow() + timedelta(hours=1)}, settings.SECRET_KEY, algorithm='HS256')
                    return JsonResponse({"message": "User logged in successfully", "token": token.decode('utf-8'), "status":200}, status=200)
                else:
                    return JsonResponse({"message": "Invalid username or password", "status":401}, status=401)
            else:
                return JsonResponse({"message": "Missing username or password", "status":400}, status=400)
        else:
            return JsonResponse({"message": "Method not allowed", "status":405}, status=405)
    except Exception as e:
        return JsonResponse({"message": "An error occurred", "status":500}, status=500)
    
@csrf_exempt
@verify_token
def get_inventory_details(request):
    try:
        items_per_page = 10
        page_number = int(request.GET.get('page', 1))
        skip = (page_number - 1) * items_per_page
        inventory_data = list(inventory.find({}).skip(skip).limit(items_per_page))
        serialized_data = [json.loads(json_util.dumps(item)) for item in inventory_data]
        total_records = inventory.count_documents({})  
        
        total_pages = math.ceil(total_records / items_per_page)
        
        response_data = {
                "message": "Data Listed successfully",
                "data": serialized_data,
                "status": 200,
                "current_page": page_number,
                "total_pages": total_pages,
                "total_records": total_records
            }
        return JsonResponse(response_data, status=200)
    except Exception as e:
        print("An error occurred:", str(e))
        return JsonResponse({"message": "An error occurred", "status":500}, status=500)

# @csrf_exempt
# @verify_token
# def get_inventory_details(request):
#     try:
#         items_per_page = 10
#         page_number = 1
#         skip = (page_number - 1) * items_per_page
#         inventory_data = list(inventory.find({}).skip(skip).limit(items_per_page))

#         return JsonResponse({"message": "Data Listed successfully", "data": inventory_data, "status":200}, status=200)

#     except Exception as e:
#         print("An error occurred:", str(e))
#         return JsonResponse({"message": "An error occurred", "status":500}, status=500)

@csrf_exempt
@verify_token
def save_inventory_details(request):
    try:
         if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            system_spec_id = data.get('system_spec_id')
            system_info = data.get('system_info')
            if(system_spec_id):
                existing_document = inventory.find_one({"system_spec_id": system_spec_id})
                if existing_document:
                    print("update new document")
                    
                    inventory.update_one(
                        {"_id": existing_document["_id"]},
                        {
                            "$set": {
                                "updated_by": request.user_id,
                                "updated_at": datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
                                "system_info": str(system_info),
                            }
                        }
                    )
                    return JsonResponse({"message": "Data Updated successfully", "status":200}, status=200)
            else:
                data = {
                    "system_spec_id": str(uuid.uuid4()),
                    "user_id": str(request.user_id),
                    "created_by": str(request.user_id),
                    "created_at": datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
                    "system_info": str(system_info),
                    "status": True
                }
                inventory.insert_one(data)
                return JsonResponse({"message": "Data Saved successfully", "status":200}, status=200)
         else:
            return JsonResponse({"message": "Method not allowed", "status":405}, status=405)
        
    except Exception as e:
        print("An error occurred:", e)
        return JsonResponse({"message": "An error occurred", "status":500}, status=500)


# def verify_token(request):
#     try:
#         token = request.META.get('HTTP_AUTHORIZATION')
#         if not token:
#             return JsonResponse({"message": "Token is missing"}, status=401)

#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
#         user_id = payload['user_id']
#         return user_id
#         # return JsonResponse({"message": "An error occurred", "status":user_id}, status=200)
#     except jwt.ExpiredSignatureError as ExpiredSignatureError:
#         # return JsonResponse({"message": "ExpiredSignatureError"}, status=200)
#         return None
#     except jwt.DecodeError as DecodeError:
#         # return JsonResponse({"message": "DecodeError"}, status=200)
#         return None


