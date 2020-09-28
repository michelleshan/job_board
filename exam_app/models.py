from django.db import models
from datetime import datetime, date, time
import re

class UserManager(models.Manager):
    def create_validator(self,requestPOST):
        errors = {}
        if len(requestPOST['first_name']) < 2 or len(requestPOST['last_name']) < 2:
            errors['short_name'] = "Both first and last name must be at least 2 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(requestPOST['email']):          
            errors['email'] = "Invalid email address!"
        existing_emails = User.objects.filter(email=requestPOST['email'])
        if len(existing_emails) > 0:
            errors['duplicate_email'] = "Email already belongs to a registered user"
        if len(requestPOST['password']) < 8:
            errors['password'] = "Password is too short"
        if requestPOST['password'] != requestPOST['confirm_pw']:
            errors['no_match'] = "Password and Password Confirmation must match"
        return errors
    def login_validators(self,requestPOST):
        errors = {}
        existing_emails = User.objects.filter(email=requestPOST['email'])
        if len(existing_emails) < 1:
            errors['no_email'] = "This email is not registered in the database."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class JobManager(models.Manager):
    def create_validator(self,requestPOST):
        errors = {}
        if len(requestPOST['title']) < 3:
            errors['short_title'] = "Title must be at least 3 characters"
        if len(requestPOST['desc']) < 10:
            errors['short_desc'] = "Description must be at least 10 characters"
        if len(requestPOST['location']) < 1:
            errors['blank_location'] = "Location cannot be blank"
        return errors
    def edit_validator(self,requestPOST):
        errors = {}
        if len(requestPOST['new_title']) < 3:
            errors['short_title'] = "Title must be at least 3 characters"
        if len(requestPOST['new_desc']) < 10:
            errors['short_desc'] = "Description must be at least 10 characters"
        if len(requestPOST['new_location']) < 1:
            errors['blank_location'] = "Location cannot be blank"
        return errors

class Job(models.Model):
    title = models.CharField(max_length=50)
    desc = models.TextField()
    location = models.CharField(max_length=100)
    owner = models.ForeignKey(User,related_name='jobs_owned',on_delete=models.CASCADE)
    workers = models.ManyToManyField(User,related_name='jobs_worked')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = JobManager()
