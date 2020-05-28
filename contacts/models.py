from django.db import models
from datetime import datetime

# Create your models here.
class Contact(models.Model):
    fullname = models.CharField(max_length=200)
    email = models.CharField(max_length=50)
    message = models.TextField(blank=False)
    contact_date = models.DateTimeField(default=datetime.now, blank=False)
    user_id = models.IntegerField(blank=True)

    def __str__(self):
        return self.fullname

