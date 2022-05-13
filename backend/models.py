from django.db import models

# Create your models here.
class Utilizador(models.Model):
    email = models.EmailField(max_length=254, primary_key=True)
    name = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    isStaff = models.BooleanField(default=False)
    isWorking = models.BooleanField(default=False)

    def __str__(self):
        return self.email
