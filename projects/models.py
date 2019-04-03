from django.db import models
from django.contrib.auth.models import User
from url_or_relative_url_field.fields import URLOrRelativeURLField
from datetime import datetime
from tinymce.models import HTMLField

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_photos',null=True,blank=True)
    bio = HTMLField()
    contact=models.CharField(max_length=12)
    projects = models.ForeignKey('Project',on_delete=models.CASCADE,null=True)

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    def update_bio(self,bio):
        self.bio = bio
        self.save()

    def __str__(self):
        return self.user.username


