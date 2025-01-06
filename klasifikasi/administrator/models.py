from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.usernamesa
    
class DataNanas(models.Model):
    sample = models.IntegerField()
    red = models.IntegerField()
    green = models.IntegerField()
    blue = models.IntegerField()
    brix = models.FloatField()
    label = models.CharField(max_length=1)

    def __str__(self):
        return f"Sample {self.sample} - {self.label}"
