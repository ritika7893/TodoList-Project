from django.contrib.auth.hashers import make_password, check_password
from django.db import models


from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    todo_name = models.TextField(max_length=255)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.todo_name
