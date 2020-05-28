from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
STATUS = (
    (0,"Draft"),
    (1,"Publish")
)
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank= True, null=True)
    updated_on = models.DateTimeField(auto_now= True)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(choices=STATUS, default=0)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)

    class Meta:
        ordering = ['-published_date']

    def publish(self):
        self.published_date=timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)

class Article(models.Model):
    author = models.CharField(max_length=250, blank = True)
    title = models.CharField(max_length=250)
    article = models.TextField(blank=False)
    article_date = models.DateTimeField(default=datetime.now, blank=False)
    


class Prayer(models.Model):
    username = models.CharField(max_length=200, blank= True)
    prayer = models.TextField(blank=True)
    prayer_date = models.DateTimeField(default=datetime.now, blank=False)
    

    
