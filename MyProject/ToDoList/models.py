from django.db import models

# Create your models here.

class UserTB(models.Model):
    Name = models.CharField(max_length=20)
    Username = models.CharField(max_length=20, unique=True)
    Email = models.EmailField(unique=True, primary_key=True)
    Password = models.CharField(max_length=20)

class TasksTB(models.Model):
    user = models.ForeignKey(
        UserTB,
        on_delete=models.CASCADE
    )
    Title = models.CharField(max_length=20)
    Description = models.TextField()
    Status = models.BooleanField(default=False)