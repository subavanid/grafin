# Create your models here.
from django.db import models
from djongo import models
from bson import ObjectId
from django.contrib.auth.models import User

from django.contrib.auth.models import AbstractUser
from djongo import models as djongo_models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

  

class Home(models.Model):
    mongodb_id = models.CharField(max_length=24, unique=True)  # Define the MongoDB ObjectId field
    room = models.CharField(max_length=100)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey field to link to the User model

    def save(self, *args, **kwargs):
        if not self.mongodb_id:
            self.mongodb_id = str(ObjectId())
        super().save(*args, **kwargs)


class HomeAppliance(models.Model):
    name = models.CharField(max_length=250)
    switchname = models.CharField(max_length=250)
    room = models.ForeignKey(Home, on_delete=models.CASCADE)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # ForeignKey field to link to the User model
    mongodb_id = models.CharField(max_length=24, null=True, blank=True)  # Define mongodb_id field

    def save(self, *args, **kwargs):
        if not self.mongodb_id:
            self.mongodb_id = str(ObjectId())
        super().save(*args, **kwargs)

    # def __str__(self):
    #     return f"{self.name} in {self.room.room}"

class HomeApplianceStatus(models.Model):
    name = models.CharField(max_length=250)
    appliance = models.CharField(max_length=24)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    sensor_reading = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.appliance} - {self.name} - {self.status} at {self.timestamp}"
    


class Office(models.Model):
    mongodb_id = models.CharField(max_length=24, unique=True)
    officeroom = models.CharField(max_length=250)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.mongodb_id:
            self.mongodb_id = str(ObjectId())
        super().save(*args, **kwargs)


class OfficeAppliance(models.Model):
    name = models.CharField(max_length=250)
    switchname = models.CharField(max_length=250)
    officeroom = models.ForeignKey(Office, on_delete=models.CASCADE)
    mongodb_id = models.CharField(max_length=24, null=True, blank=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.mongodb_id:
            self.mongodb_id = str(ObjectId())
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} in {self.officeroom.officeroom}"


class OfficeApplianceStatus(models.Model):
    appliance_id = models.CharField(max_length=24)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    sensor_reading = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.appliance_id} - {self.status} at {self.timestamp}"



