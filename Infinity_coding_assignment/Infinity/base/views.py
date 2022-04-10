from django.urls import path
from django.shortcuts import render, redirect
import pyrebase
from django.contrib import messages, auth
from datetime import datetime, timezone
import time
import pytz

# Create your views here.

config = {
    "apiKey": "AIzaSyAQA7BvYdXtFGxZryTYjz2B4lQYRC4ei_k",
    "authDomain": "infinity-coding-assignment.firebaseapp.com",
    "databaseURL": "https://infinity-coding-assignment-default-rtdb.firebaseio.com/",
    "projectId": "infinity-coding-assignment",
    "storageBucket": "infinity-coding-assignment.appspot.com",
    "messagingSenderId": "862463656109",
    "appId": "1:862463656109:web:1a2c439f6e3ee9bd6d4624",
    "measurementId": "G-QBP4EEHNLE"
  };

firebase = pyrebase.initialize_app(config)
pyre_auth = firebase.auth()
database = firebase.database()
login_user = None
user = None

def login(request):
    # login section    
    if request.method == 'POST':
        # login section
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            login_user = pyre_auth.sign_in_with_email_and_password(email, password)
            
        except:
            messages.error(request, 'Wrong email address or password.')
            return redirect("login")

        print(login_user['idToken']) 
        session_id = login_user['idToken']  
        request.session['uid'] = str(session_id)

        idToken = request.session['uid']
        u = pyre_auth.get_account_info(idToken)
        u = u['users']
        u = u[0]
        u = u['localId']

        name = database.child('users').child(u).child('account info').child('username').get().val()
        return render(request, 'home.html', {'login_user': name})

    return render(request, 'login.html')

def signup(request):
    # signup section
    if request.method == 'POST':
        now = datetime.now()
        registered_date = now.strftime("%d/%m/%Y %H:%M:%S")
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = pyre_auth.create_user_with_email_and_password(email, password)
            

        except:
            messages.error(request, "Something's wrong! Please sign up again.")
            return redirect("signup")

        uid = user['localId']    
        user_data = {
                        "user_id": uid,
                        "username": username,
                        "email": email,
                        "password": password,
                        "registered_date": registered_date
                    }

        database.child("users").child(uid).child("account info").set(user_data)

        user_todolist = {}

        database.child("users").child(uid).child("lists").set(user_todolist)
        return render(request, 'login.html')
       
    return render(request, 'signup.html')


def home(request):
    # login section
    email = request.POST.get('email')
    password = request.POST.get('password')

    try:
        login_user = pyre_auth.sign_in_with_email_and_password(email, password)
        
    except:
        messages.error(request, 'Wrong email address or password.')
        return redirect("login")

    print(login_user['idToken']) 
    session_id = login_user['idToken']  
    request.session['uid'] = str(session_id)

    idToken = request.session['uid']
    u = pyre_auth.get_account_info(idToken)
    u = u['users']
    u = u[0]
    u = u['localId']
        
    name = database.child('users').child(u).child('account info').child('username').get().val()
    return render(request, 'home.html', {'login_user': name})

def add_plan(request):
    idToken = request.session['uid']
    u = pyre_auth.get_account_info(idToken)
    u = u['users']
    u = u[0]
    u = u['localId']

    if request.method == 'POST':
        tz = pytz.timezone('Asia/Kuala_Lumpur')
        plan_created_date = datetime.now(timezone.utc).astimezone(tz)
        millis = int(time.mktime(plan_created_date.timetuple()))
        # Add toda list section
        plan = request.POST.get('plan')

        plan_data = {
            "plan": plan
        }

        database.child('users').child(u).child('lists').child(millis).set(plan_data)

    
    #Retrieve data from realtime database
    task_no = database.child('users').child(u).child('lists').shallow().get().val()
    if not task_no is None:
        list_tasks = []
        for i in task_no: 
            list_tasks.append(i)

        print('list_tasks:',list_tasks)

        plans = []
        for i in list_tasks:
            p = database.child('users').child(u).child('lists').child(i).child('plan').get().val()
            plans.append(p)

        tasks = zip(list_tasks, plans)
        return render(request, 'addplan.html', {'tasks':tasks})

    return render(request, 'addplan.html')

def viewPlan(request):
    
    idToken = request.session['uid']
    u = pyre_auth.get_account_info(idToken)
    u = u['users']
    u = u[0]
    u = u['localId']

    print('u:',u)

    #Delete data from realtime database
    task_no = database.child('users').child(u).child('lists').shallow().get().val()
    if not task_no is None:
        if request.method == 'POST':
            remove = request.POST.get('remove')
            database.child('users').child(u).child('lists').child(remove).remove()

        list_tasks = []
        for i in task_no: 
            list_tasks.append(i)

        print('list_tasks:',list_tasks)

        plans = []
        for i in list_tasks:
            p = database.child('users').child(u).child('lists').child(i).child('plan').get().val()
            plans.append(p)

        tasks = zip(list_tasks, plans)
        return render(request, 'viewPlan.html', {'tasks':tasks})

    return render(request, 'viewPlan.html')

def logout(request):
    auth.logout(request)
    return render(request, 'login.html')
