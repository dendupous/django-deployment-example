from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfileInfor(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE) #on_delete=models.CASCADE

    #additional classes
    portfolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)

    def __str__(self):
        return self.user.username()
