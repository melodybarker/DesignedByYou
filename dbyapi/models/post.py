from django.db import models
from .diyuser import DiyUser
from .category import Category
class Post(models.Model):
    """Post Model"""

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="post_category")
    title = models.CharField(max_length=50)
    content = models.TextField()
    image_url = models.URLField(default="https://upload.wikimedia.org/wikipedia/commons/8/89/Portrait_Placeholder.png")
    date = models.DateTimeField(auto_now_add=True)
    diyuser = models.ForeignKey(DiyUser, on_delete=models.CASCADE, related_name="posts")