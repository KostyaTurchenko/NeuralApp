from django.shortcuts import render
import pyrebase
from django.contrib import auth
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

def signIn(request):

    return render(request, "index.html")

def postsign(request):
    email=request.POST.get('email')
    passw = request.POST.get("pass")
    try:
        user = authe.sign_in_with_email_and_password(email,passw)
    except:
        message="invalid credentials"
        return render(request,"index.html",{"messg":message})
    print(user['idToken'])
    session_id=user['idToken']
    request.session['uid']=str(session_id)
    return render(request, "admin.html",{"e":email})
def logout(request):
    auth.logout(request)
    return render(request,'index.html')


