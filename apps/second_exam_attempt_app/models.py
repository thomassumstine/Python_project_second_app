from django.db import models

# Create your models here.
from django.db import models
from helpers import stringify_dict
# Create your models here.


class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 320)
    password = models.CharField(max_length = 60)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def full_name(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return stringify_dict(self.__dict__)




class Jobs(models.Model):
    job_title = models.CharField(max_length=255)
    job_description = models.CharField(max_length=255)
    job_location = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, related_name="created_jobs")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return stringify_dict(self.__dict__)