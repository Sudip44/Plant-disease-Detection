from django.urls import path
from tomato import views

urlpatterns=[
    path('tomato/',views.index,name='tomato'),
    
]