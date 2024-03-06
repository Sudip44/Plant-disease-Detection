from django.urls import path
from firstapp import views

urlpatterns=[
    #path('/rice',views.index,name='rice'),
    path('',views.index,name='rice'),
    
]