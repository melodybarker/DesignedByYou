from datetime import date
from email import contentmanager


from django.db import models
from .post import Post
from .diyuser import DiyUser

class Comment(models.Model):

  content = models.CharField(max_length=250)
  date = models.DateTimeField(auto_now_add=True)
  post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
  user = models.ForeignKey(DiyUser, on_delete=models.CASCADE, related_name="comments")