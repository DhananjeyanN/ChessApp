from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/')
    dob = models.DateField(null=True, blank=True)
    is_logged_in = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} {self.user.email}'


class SiteProfile(models.Model):
    name = models.CharField(max_length=100)
    about = models.TextField()
    developed_by = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='core_images/')
    h1 = models.ImageField(upload_to='core_images/', blank=True)
    h2 = models.ImageField(upload_to='core_images/', blank=True)
    photos = models.ImageField(upload_to='core_images/', blank=True)
    photos2 = models.ImageField(upload_to='core_images/', blank=True)
    photos3 = models.ImageField(upload_to='core_images/', blank=True)
    photos4 = models.ImageField(upload_to='core_images/', blank=True)
    year_started = models.DateField()

    def __str__(self):
        return self.name