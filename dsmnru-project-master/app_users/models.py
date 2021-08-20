from django.db import models
from django.contrib.auth.models import User
import os
from django.urls import reverse

def path_and_rename(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = 'User_Profile_Pictures/{}.{}'.format(instance.pk, ext)
    return os.path.join(upload_to, filename)


def logo_name(instance, filename):
    upload_to = 'Logo/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = 'Logo/{}.{}'.format(instance.pk, ext)
    return os.path.join(upload_to, filename)


class UserProfileInfo(models.Model):
    class Meta:
        verbose_name_plural = "User Profile Info"

    #creating a relationship with user class (not inheriting)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    #adding additional attributes
    bio = models.CharField(max_length=500,blank=True)
    profile_pic = models.ImageField(upload_to=path_and_rename, verbose_name="Profile Picture", blank=True)
    teacher = 'teacher'
    student = 'student'
    user_types = [
        (teacher, 'teacher'),
        (student, 'student')
    ]
    user_type = models.CharField(max_length=10, choices=user_types, default=student)

    def __str__(self):
        return self.user.username

class Query(models.Model):
    class Meta:
        verbose_name_plural = "Query"

    name = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    message = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('index')

class AboutUs(models.Model):
    class Meta:
        verbose_name_plural =  "About Us"

    text = models.TextField(max_length = 500)
    dateCreated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50] + " ...." + " Posted on: " + str(self.dateCreated)

class Logo(models.Model):
    class Meta:
        verbose_name_plural = "Logo"

    name = name = models.CharField(max_length = 50)
    image = models.ImageField(upload_to=logo_name, verbose_name="Logo Image")
    dateCreated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + " Posted on: " + str(self.dateCreated)

class Contact(models.Model):
    class Meta:
        verbose_name_plural = "Contact"

    entry = models.CharField(max_length=100)
    dateCreated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.entry + " Posted on: " + str(self.dateCreated)


class ContactForm(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=500)
    message = models.TextField()
    postDate = models.DateField()

    def __str__(self):
        return self.name + " Posted on: " + str(self.postDate)