from django.db import models
# from django.contrib.auth.models import User

# Create your models here.
class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    
class SystemSpec(models.Model):
    system_spec_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    system_info = models.JSONField()
    deleted_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=50)