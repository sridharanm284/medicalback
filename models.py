from django.db import models

# Create your models here.


class Login(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    user_type = models.CharField(max_length=10)  # 'doctor' or 'patient'
