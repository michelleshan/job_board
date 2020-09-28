from django.shortcuts import render, redirect, HttpResponse
from .models import User, Job
from django.contrib import messages
import bcrypt
from django.db.models import Count

def index(request):
    return render(request,'index.html')

def create_user(request):
    if request.method == 'POST':
        errors = User.objects.create_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                return redirect('/')
        else:
            hashed_pw = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()
            some_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hashed_pw)
            request.session['user_id'] = some_user.id
    return redirect('/dashboard')

def login(request):
    if request.method == "POST":
        registered_emails = User.objects.filter(email=request.POST['email'])
        if registered_emails:
            some_user = registered_emails[0]
            if bcrypt.checkpw(request.POST['password'].encode(),some_user.password.encode()):
                request.session['user_id'] = some_user.id
                return redirect('/dashboard')
            else:
                print("Password didn't match")
                messages.error(request, "Incorrect name or password")
        else:
            print("Email not found")
            messages.error(request, "Incorrect name or password")
    return redirect('/')

def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        some_user = User.objects.get(id=request.session['user_id'])
        context = {
            'some_user': User.objects.get(id=request.session['user_id']),
            'jobs': Job.objects.all(),
            'some_user_jobs': some_user.jobs_worked.all()
        }
        return render(request,'dashboard.html',context)

def destroy(request):
    del request.session['user_id']
    return redirect('/')

def add_job(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        return render(request,'add_job.html')

def create_job(request):
    if request.method == 'POST':
        errors = Job.objects.create_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                return redirect('/addJob')
        else:
            Job.objects.create(
                title = request.POST['title'],
                desc = request.POST['desc'],
                location = request.POST['location'],
                owner = User.objects.get(id=request.session['user_id'])
            )
        return redirect('/dashboard')

def view_job(request,id):
    some_job = Job.objects.filter(id=id)
    if some_job:
        job = some_job[0]
        context = {
            'some_job' : Job.objects.get(id=id),
            'some_user_jobs' : User.objects.get(id=request.session['user_id']).jobs_worked.all()
        }
        return render(request,'view_job.html',context)
    else:
        return redirect('/dashboard')

def add_to_my_jobs(request,id):
    if request.method == 'GET':
        some_job = Job.objects.get(id=id)
        some_user = User.objects.get(id=request.session['user_id'])
        some_user.jobs_worked.add(some_job)
        return redirect('/dashboard')

def remove_from_my_jobs(request,id):
    if request.method == 'GET':
        some_job = Job.objects.get(id=id)
        some_user = User.objects.get(id=request.session['user_id'])
        some_user.jobs_worked.remove(some_job)
        return redirect('/dashboard')

def edit_job(request,id):
    if 'user_id' not in request.session:
        return redirect('/')
    some_job = Job.objects.filter(id=id)
    some_user = User.objects.get(id=request.session['user_id'])
    if some_job:
        job = some_job[0]
        if some_user != job.owner:
            return redirect('/dashboard')
        else:
            context = {
                'some_job': Job.objects.get(id=id)
            }
        return render(request,'edit_job.html',context)
    else:
        return redirect('/dashboard')

def update_job(request,id):
    if request.method == 'POST':
        errors = Job.objects.edit_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                return redirect(f'/edit/{id}')
        else:
            some_job = Job.objects.get(id=id)
            some_job.title = request.POST['new_title']
            some_job.desc = request.POST['new_desc']
            some_job.location = request.POST['new_location']
            some_job.save()
            print('saved job updates')
        return redirect('/dashboard')

def cancel_job(request,id):
    Job.objects.get(id=id).delete()
    return redirect('/dashboard')