from __future__ import unicode_literals

from django.db import models
import re, bcrypt

class UserManager(models.Manager):
    def validUser(self, post):
        valid = True
        errors = []
        if len(post.get('name')) == 0:
            errors.append('Name must not be empty.')
            valid = False
        if len(post.get('username')) == 0:
            errors.append('Username must not be empty.')
            valid = False
        if len(post.get('email')) == 0:
            errors.append('Email must not be empty.')
            valid = False
        if len(post.get('password')) == 0:
            errors.append('Password must not be empty.')
            valid = False
        if post.get('cpassword') != post.get('password'):
            errors.append('User Password and Confirmation do not Match.')
            valid = False
        return {"status" : valid, "Errors" : errors}



    def userCreate(self, post):
        return User.objects.create(
            name = post.get('name'),
            userName = post.get('username'),
            email = post.get('email'),
            password = bcrypt.hashpw(post.get('password').encode(),bcrypt.gensalt())
        )



    def checkUser(self, post):
        valid = True
        errors = []
        user = User.objects.filter(email = post.get('logemail')).first()

        if len(post.get('logemail')) == 0:
            errors.append('Email must not be empty.')
            valid = False
        if len(post.get('logpassword')) == 0:
            errors.append('Enter Password.')
            valid = False
        if not user:
            errors.append('Email not found in Database.')
            valid = False
        if valid != False:
            if bcrypt.hashpw(post.get('logpassword').encode(), user.password.encode()) != user.password:
                errors.append('Email and Password do not Match.')
                valid = False
            else:
                return {'status': True, 'user': user}
        return {"status" : valid, "Errors" : errors}



class DestManager(models.Manager):
    def validDest(self, post, currentUser):
        valid = True
        errors = []

        if len(post.get('destination')) == 0:
            messages.append('Name of Destination must not be empty.')
            valid = False
        if len(post.get('description')) == 0:
            messages.append('Description must not be empty.')
            valid = False
        if len(post.get('plan')) == 0:
            messages.append('Enter some Plans or just put *.')
            valid = False
        if len(post.get('from')) == 0:
            messages.append('Date From must not be empty.')
            valid = False
        if len(post.get('until')) == 0:
            messages.append('Date Until must not be empty.')
            valid = False


        return {"status" : valid, "Errors" : errors}


    def destCreator(self, post, currentUser):
        return Destinations.objects.create(
            destName = post.get('destination'),
            destDescription = post.get('description'),
            destPlan = post.get('plan'),
            dateFrom = post.get('from'),
            dateUntil = post.get('until'),
            plannedBy = currentUser
        )


class User(models.Model):
    name = models.CharField(max_length=255)
    userName = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    cPassword = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __str__(self):
        return self.name + " " + self.userName + " " + self.email

class Destinations(models.Model):
    destName = models.CharField(max_length=255)
    destDescription = models.CharField(max_length=255)
    destPlan = models.CharField(max_length=255)
    dateFrom = models.CharField(max_length=255)
    dateUntil = models.CharField(max_length=255)
    plannedBy = models.ForeignKey(User, related_name = "plannedFor")
    joinedBy = models.ManyToManyField(User, related_name = "joined")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = DestManager()
