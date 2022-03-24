from django.db import models
from django.contrib.auth.models import User


class DiyUser(models.Model):
    """DiyUser Model"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="diy_user")
    image_url = models.URLField()
    bio = models.CharField(max_length=500, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    # likes = models.ManyToManyField('dbyapi.Like', on_delete=models.CASCADE, related_name="liked_post")