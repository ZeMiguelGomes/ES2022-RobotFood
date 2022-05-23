from django.db import models

# Create your models here.
class Staff(models.Model):
    staff_email = models.EmailField(primary_key=True)
    staff_name = models.CharField("name", max_length=240)
    password = models.CharField("password", max_length=240)
    authToken = models.TextField(blank=True, null=True)
    isLoggedIn = models.CharField(default='False', max_length=240)
    
    def __str__(self):
        return self.staff_email