from django.http import JsonResponse
from django.views import View
from pymongo import MongoClient
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import logging
import re
from .models import Email

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class MyDataView(View):
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

    def post(self, request):
        try:
            client = MongoClient('mongodb+srv://root:RHVvLbi5tJgqUxzm@cluster0.lq35h.mongodb.net')
            db = client['grader']
            collection = db['user']

            if request.content_type == 'application/json':
                new_data = json.loads(request.body)
            else:
                new_data = request.POST

            # Validate and retrieve email
            if 'email' in new_data:
                email = new_data['email']

                if not self.is_valid_email(email):
                    return JsonResponse({"error": "Invalid email format."}, status=400)
                
                # Insert into MongoDB 
                if not collection.find_one({'email': email}):
                    result = collection.insert_one({'email': email})
                    logger.info(f"Data inserted with id: {result.inserted_id}")
                
                # Insert into admin
                Email.objects.get_or_create(email_address=email)

                return JsonResponse({"message": "Email saved successfully!"}, status=201)
            else:
                return JsonResponse({"error": "Email is required."}, status=400)

        except Exception as e:
            logger.error(f"Error in POST request: {e}")
            return JsonResponse({"error": str(e)}, status=400)

    def is_valid_email(self, email):
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(regex, email) is not None
