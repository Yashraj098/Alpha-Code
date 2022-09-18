from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField



# Create your models here.
class Blog(models.Model):
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to='blog/images/')
    description=RichTextField(blank=True,null=True)
    date=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title