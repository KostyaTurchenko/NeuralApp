from django.urls import path
from . import views

urlpatterns = [
    path('image/', views.PostView.as_view(), name= 'image_list'),
    path('config/', views.ConfigView.as_view(), name= 'config_list'),

]