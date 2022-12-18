from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User,Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from sqlalchemy import create_engine
from csvs.views import *
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from .models import user_database
from django.views.decorators.clickjacking import xframe_options_sameorigin
# Create your views here.
#=================================================================================================================
"""
type    : function
name    : signup
html    : signup.html
path    : 'user_manage/signup/' 
"""
# @xframe_options_sameorigin
def signup(request):
    if request.user.is_superuser:
        if request.method == "POST" :
            username = request.POST.get('username',False)
            fname = request.POST.get('fname',False)
            lname = request.POST.get('lname',False)
            email = request.POST.get('email',False)
            pass1 = request.POST.get('pass1',False)
            pass2 = request.POST.get('pass2',False)
            group = request.POST['group']
            
            if User.objects.filter(username=username):
                messages.error(request, "Username already exist! Please try some other username.")
                return redirect('login:signup')
            
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email Already Registered!!")
                return redirect('login:signup')
            
            if len(username)>20:
                messages.error(request, "Username must be under 20 charcters!!")
                return redirect('login:signup')
            
            if pass1 != pass2:
                messages.error(request, "Passwords didn't matched!!")
                return redirect('login:signup')
            
            if not username.isalnum():
                messages.error(request, "Username must be Alpha-Numeric!!")
                return redirect('login:signup')
            user2 = request.user.is_superuser
            myuser = User.objects.create_user(username, email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.is_active = True
            myuser.is_staff = False
            myuser.save()
            my_group = Group.objects.get(name=f'{group}') 
            your_user = User.objects.get(username = f'{username}')
            my_group.user_set.add(your_user)
            my_group.save()
            group = str(group).lower().replace(' ','_')
            user_database.objects.create(username = username,password = encryptfunc(pass1),group = group).save()
            group = group.replace('_dwh','')
            sol = []
            conn = dbconfserver().connect()
            conn.execute(f"create user {username} with password '{pass1}';")
            conn.execute(f"ALTER GROUP {group} ADD USER {username};")
            for i in conn.execute("select datname from pg_catalog.pg_database;"):
                result = (multiple_replace(str(i),{'(':'',')':'',"'":'',',':'','_view':'',' ':'.'}))
                sol.append(result)
            for j in sol:
                conn.execute(f"REVOKE ALL ON DATABASE {j} FROM {group};")
            conn.execute(f"GRANT  ALL ON DATABASE {group} TO {group};")
            conn.execute(f"GRANT ALL PRIVILEGES ON SCHEMA csv TO {group};")
            conn.close()
            messages.success(request, "Your Account has been created succesfully!!")
            return render(request, "signup.html",{'user':user2})
        else:
           return render(request, "signup.html")
    else:
        messages.error(request,"anda bukan admin")
        return redirect("login:signin")
#=================================================================================================================
"""
type    : function
name    : signin
html    : login.html,indexinp.html
path    : 'user_manage/login/' 
"""
def signin(request):
    if request.method == 'POST':
        if request.POST.get("form_sigup") == 'signup':
            #sign up from model
            username = request.POST.get('username',False)
            fname = request.POST.get('fname',False)
            lname = request.POST.get('lname',False)
            email = request.POST.get('email',False)
            pass1 = request.POST.get('pass1',False)
            pass2 = request.POST.get('pass2',False)
            
            if User.objects.filter(username=username):
                messages.error(request, "Username already exist! Please try some other username.")
                return redirect('login:signin')
            
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email Already Registered!!")
                return redirect('login:signin')
            
            if len(username)>20:
                messages.error(request, "Username must be under 20 charcters!!")
                return redirect('login:signin')
            
            if pass1 != pass2:
                messages.error(request, "Passwords didn't matched!!")
                return redirect('login:signin')
            
            if not username.isalnum():
                messages.error(request, "Username must be Alpha-Numeric!!")
                return redirect('login:signin')

            user_database.objects.create(username = username,password = encryptfunc(pass1)).save()
            myuser = User.objects.create_user(username, email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.is_active = True
            myuser.is_staff = False
            myuser.save()
            conn = dbconfserver().connect()
            conn.execute(f"create user {username} with password '{pass1}';")
            conn.execute(f"ALTER GROUP not_org_dwh ADD USER {username};")
            conn.execute(f"GRANT ALL PRIVILEGES ON SCHEMA csv TO not_org_dwh;")
            conn.close()
            messages.success(request, "Your Account has been created succesfully!!")
            return redirect('login:signin')
        else:
            #backend login
            try:
                username = request.POST['user']
                pass1 = request.POST['pass']
                user2 = authenticate(username=username, password=pass1)
                if user2 is not None:
                    login(request, user2)
                    fname = user2.first_name
                    messages.success(request, "Logged In Sucessfully!!")
                    return render(request, "indexinp.html",{"fname":user2})
            except:
                messages.error(request,'username atau password anda salah')
                return redirect('login:signin')
    else:
        if request.user.is_authenticated:
            user2 = request.user.get_username()
            return render(request, "indexinp.html",{"fname":user2})
        else:
            return render(request, "login.html")
#=================================================================================================================
"""
type    : function
name    : signout
html    : login.html,indexinp.html
path    : 'user_manage/signout/' 
"""
@login_required
def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect("login:signin")
#=================================================================================================================
"""
type    : function
name    : profile
html    : profile.html
path    : 'user_manage/profile/' 
"""
def profile(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            username= request.user.get_username()
            full_name= request.user.get_full_name()
            email= request.user.email 
            db,user,passw = dblog(request)
            content = {
                'username':username,
                'full_name':full_name,
                'email':email
            }
            return render(request,'profile.html',content)
    else:
        messages.error(request,"silahkan login terlebih dahulu")
        return redirect("login:signin")
#=================================================================================================================
"""
type    : function
name    : delete_user
html    : delete_user.html
path    : 'user_manage/delete_user/' 
"""
def delete_user(request):
    if request.user.is_superuser:
        if request.method == "POST":
            delete_user_post = request.POST['delete_user']
            user = []
            for i in list(User.objects.all()):
                result = (multiple_replace(str(i),{'<User:':'','>,':'','admin':''}))  
                if result not in 'admin': 
                    user.append(user)
            User.objects.get(username = f'{delete_user_post}').delete()
            conn = dbconfserver().connect()
            user_exists  = conn.execute(f"SELECT 1 FROM pg_roles WHERE rolname='{delete_user_post}';").rowcount > 0
            if user_exists  is True:
                conn.execute(f"DROP ROLE {delete_user_post};")
            else:
                None
            messages.success(request,'user berhasil dihapus')
            contex = {
                'user':user
            }
            return render(request,'delete_user.html',contex)
        else:
            user = []
            for i in list(User.objects.all()):
                result = (multiple_replace(str(i),{'<User:':'','>,':'','admin':''}))  
                if result not in 'admin': 
                    user.append(result)
            print(user)
            contex = {
                'user':user
            }
            return render(request,'delete_user.html',contex)
    else:
        messages.error(request,"anda bukan admin")
        return redirect("csv_data:transfer")
#=================================================================================================================
"""
type    : function
name    : create_org
html    : create_org.html
path    : 'user_manage/create_org/' 
"""
def create_org(request):
    if request.user.is_superuser:
        if request.method == "POST":
            namegroup = request.POST['group']
            Group.objects.create(name = f'{namegroup}').save()
            conn = dbconfserver().connect()
            conn.execute(f"create database {namegroup};")
            conn.execute(f"CREATE GROUP {namegroup};")
            conn.execute(F'CREATE SCHEMA csv;')
            conn.close()
            messages.success(request,'berhasil membuat group')
            return render(request,'create_org.html')
        else:
            return render(request,'create_org.html')
    else:
        messages.error(request,"anda bukan admin")
        return redirect("csv_data:transfer")

