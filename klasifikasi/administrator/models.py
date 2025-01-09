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
    gambar = models.CharField(max_length=200)

    def __str__(self):
        return f"Sample {self.sample} - {self.label}"
    
class RiwayatKlasifikasi(models.Model):
    red = models.IntegerField()
    green = models.IntegerField()
    blue = models.IntegerField()
    brix = models.FloatField()
    label = models.CharField(max_length=10)
    gambar = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.label} - {self.created_at}"

