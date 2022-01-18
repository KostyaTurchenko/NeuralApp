from .serializers import ImageSerializer, ConfigSerializer
import os
from .models import Image, Config
import pyrebase
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.contrib import auth
from django.shortcuts import render
from django.http import HttpResponse
from api.main import predict, sendImage
import base64
from pathlib import Path
from django.views.decorators.csrf import csrf_exempt,csrf_protect
# Create your views here.


config = {
    'apiKey': "AIzaSyDBSukqEgkEgVRvyNkPx-J6Xo6fXR56Bgw",
    'authDomain': "neural-app-b3ba5.firebaseapp.com",
    'projectId': "neural-app-b3ba5",
    'storageBucket': "neural-app-b3ba5.appspot.com",
    'messagingSenderId': "378806207595",
    'appId': "1:378806207595:web:76081a82f8bdc22eed9d2e",
    'measurementId': "G-BS0DX7HQL9",
    'databaseURL': "https://cpanel-5e873.firebaseio.com",
  }

firebase = pyrebase.initialize_app(config)

authe = firebase.auth()
database=firebase.database()


def signIn(request):
    return render(request, "index.html")


def postsign(request):
    email = request.POST.get('email')
    passw = request.POST.get("pass")
    try:
        user = authe.sign_in_with_email_and_password(email, passw)
    except:
        message = "invalid credentials"
        return render(request, "index.html", {"messg": message})

    print(user['idToken'])
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    print(user['idToken'])
    return render(request, "admin_base.html", {"email": user['email']})

def logout(request):
    auth.logout(request)
    return render(request, 'index.html')

@csrf_exempt
def save_config(request):
    user = authe.current_user
    print(user['idToken'])
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    print(user['idToken'])
    if request.method == "POST":
        print(request.POST['diagram'])
        Config.objects.update(diagram=request.POST['diagram'])
        Config.objects.update(dropout=request.POST['dropout'])
        Config.objects.update(accuracy=request.POST['accuracy'])
    return render(request, "edit.html", {"email": user['email'], "password": 1232131312})


class PostView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        posts = Image.objects.all()
        serializer = ImageSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        image_serializer = ImageSerializer(data=request.data)
        if image_serializer.is_valid():
            image_serializer.save()
            path = image_serializer.data['image'][1:]
            result = predict(path)
            imageBase64 = sendImage()
            sendResult = []
            sendResult.append(result)
            return Response(sendResult, status=status.HTTP_201_CREATED)
        else:
            print('error', image_serializer.errors)
            return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConfigView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        configs = Config.objects.all()
        serializer = ConfigSerializer(configs, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        config_serializer = ConfigSerializer(data=request.data)
        if config_serializer.is_valid():
            config_serializer.save()
            print(config_serializer.data)
            return Response("Success", status=status.HTTP_201_CREATED)
        else:
            print('error', config_serializer.errors)
            return Response(config_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
