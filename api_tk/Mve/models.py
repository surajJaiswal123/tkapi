from django.db import models

# Create your models here.
class MvModel(models.Model):
    title = models.CharField(max_length=300)
    genre = models.CharField(max_length=150)
    release_date = models.DateField()
    director = models.CharField(max_length=150)
   