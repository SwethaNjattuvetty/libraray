from django.db import models

class Users(models.Model):
    name=models.CharField(max_length=20)
    age=models.IntegerField()
    place=models.CharField(max_length=20)
    gender=models.CharField(max_length=20)
    email=models.CharField(max_length=20)


    def __str__(self):
         return self.name

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    address=models.CharField(max_length=30,default="")
    phone=models.IntegerField(default=0)


    is_superuser = models.BooleanField(default=False)  #admin user
    is_user=models.BooleanField(default=False)        #normal user

    def __str__(self):
          return self.username