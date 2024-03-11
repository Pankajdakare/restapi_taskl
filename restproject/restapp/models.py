from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Client(models.Model):
    client_name = models.CharField(max_length = 20, default='')
    createdat = models.DateTimeField(auto_now_add=True)
    uid = models.ForeignKey( User,on_delete = models.CASCADE, db_column="uid", default =0)
    createdby = models.OneToOneField(User)

class Project(models.Model):
    project_name = models.CharField(max_length = 20, default='')
    createdat = models.DateTimeField(auto_now_add=True)
    uid = models.ForeignKey( User,on_delete = models.CASCADE, db_column="uid", default =0)
    createdby = models.OneToOneField(User)