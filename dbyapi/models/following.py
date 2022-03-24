from django.db import models
# from .diyuser import DiyUser


class Following(models.Model):

    to_diyuser = models.ForeignKey(
        'dbyapi.DiyUser', on_delete=models.CASCADE, null=False, blank=False, related_name="following")
    from_diyuser = models.ForeignKey(
        'dbyapi.DiyUser', on_delete=models.CASCADE, null=False, blank=False, related_name="followed_by")
