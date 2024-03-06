
from django.urls import path
from potaoto import views

urlpatterns=[
    path('potato/',views.index,name='potato')
]