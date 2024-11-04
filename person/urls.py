from django.urls import path
from .views import MyDataView 

urlpatterns = [
    path('api/data/', MyDataView.as_view(), name='my_data_view'),
]
