from ast import BinOp
from django.db import models
from django.contrib.auth.models import User
from platformdirs import user_cache_dir

class DiyUser(models.Model):

  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="diy_user")
  bio = models.CharField(max_length=500, null=True)
  created_on = models.DateTimeField(auto_now_add=True)