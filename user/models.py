from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, blank=False, null=False, unique=True)
    email = models.EmailField(max_length=100, blank=False, null=False, unique=True)
    password = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.username