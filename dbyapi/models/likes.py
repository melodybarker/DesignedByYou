from django.db import models
from .diyuser import DiyUser
from .post import Post


class Like(models.Model):

    diypost = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="liked_post")
    liker = models.ForeignKey(
        DiyUser, on_delete=models.CASCADE, related_name="user_likes")
