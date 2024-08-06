from django.db import models


# https://docs.djangoproject.com/en/5.0/topics/auth/customizing/


class User(models.Model):
    class Meta:
        db_table = "users"

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birth = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + " " + self.last_name + f" ({self.username})"  
