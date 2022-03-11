from pdb import post_mortem
from django.db import models
from .diyuser import DiyUser
from .category import Category

class Post(models.Model):

  category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="post_category")
  title = models.CharField(max_length=50)
  content = models.TextField()
  image = models.FileField(upload_to='photos/%Y/%m/%d')
  date = models.DateTimeField(auto_now_add=True)
  user = models.ForeignKey(DiyUser, on_delete=models.CASCADE, related_name="posts")