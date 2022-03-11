from django.db import models
from .diyuser import DiyUser


class Follow(models.Model):

  following = models.ForeignKey(DiyUser, on_delete=models.CASCADE, related_name="follows")
  follower = models.ForeignKey(DiyUser, on_delete=models.CASCADE, related_name="followed_by")