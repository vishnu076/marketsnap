from django.db import models

# Create your models here.ss

class Products(models.Model):
    pid=models.PositiveIntegerField()
    pname=models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    pbrand=models.CharField(max_length=100)
    price=models.IntegerField()
    desc=models.CharField(max_length=500)
    color=models.CharField(max_length=100)


    
