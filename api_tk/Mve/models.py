from django.db import models

# Create your models here.
class MvModel(models.Model):
    title = models.CharField(max_length=300,null=True,blank=True)
    genre = models.CharField(max_length=150,null=True,blank=True)
    release_date = models.DateField(null=True,blank=True)
    director = models.CharField(max_length=150,null=True,blank=True)
   