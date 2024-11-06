from django.http import JsonResponse
from django.views import View
from pymongo import MongoClient
from django.views.decorators.csrf import csrf_exempt
import json
import logging
import re 

logger = logging.getLogger(__name__)

class MyDataView(View):
    @csrf_exempt 
    def get(self, request):
        try:
            client = MongoClient('mongodb+srv://root:RHVvLbi5tJgqUxzm@cluster0.lq35h.mongodb.net')
            db = client['grader']  
            collection = db['user']  
            data = list(collection.find())
            data = [{**doc, "_id": str(doc["_id"])} for doc in data]
            client.close()
            return JsonResponse(data, safe=False)
        except Exception as e:
            logger.error(f"Error in GET request: {e}")
            return JsonResponse({"error": str(e)}, status=500)

    @csrf_exempt 
    def post(self, request):
        try:
            client = MongoClient('mongodb+srv://root:S@nCybySama@cluster0.lq35h.mongodb.net')
            db = client['grader']
            collection = db['user']
            
            if request.content_type == 'application/json':
                new_data = json.loads(request.body)
            else:
                new_data = request.POST
            
            if 'email' in new_data:
                email = new_data['email'] 

                if not self.is_valid_email(email):
                    return JsonResponse({"error": "Invalid email format."}, status=400)

                new_data = {'email': email} 
            else:
                return JsonResponse({"error": "Email is required."}, status=400)
            
            logger.info(f"Data received for insertion: {new_data}")

            result = collection.insert_one(new_data)
            client.close()
            
            logger.info(f"Data inserted with id: {result.inserted_id}")
            return JsonResponse({"message": "Data saved successfully!"}, status=201)
        
        except Exception as e:
            logger.error(f"Error in POST request: {e}")
            client.close()
            return JsonResponse({"error": str(e)}, status=400)

    def is_valid_email(self, email):
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(regex, email) is not None
