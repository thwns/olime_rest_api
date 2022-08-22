"""
Database models.
"""
import uuid
import os

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db.models.signals import post_save
from django.dispatch import receiver


def recipe_image_file_path(instance, filename):
    """Generate file path for new recipe image."""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'recipe', filename)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Profile(models.Model):
    USER = 1
    LEADER = 2
    ADMIN = 3
    ROLE_CHOICES = (
        (USER, 'User'),
        (LEADER, 'Leader'),
        (ADMIN, 'Admin'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, unique=True, on_delete=models.CASCADE,)
    nickname = models.CharField(max_length=225)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True, blank=True)
    subjects = models.CharField(max_length=225)
    image_url = models.CharField(max_length=225)
    #followed_tracks = models.ManyToManyField('Track', blank =True)

    def __str__(self):
        return self.user.nickname


class UserDate(models.Model):
    track = models.ForeignKey(
        'track',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    action_date =
    order_major =


class Track(models.Model):
    """Trkack object."""
    leader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    profile = models.ForeignKey(
        'Profile',
        on_delete=models.CASCADE,
        blank=True
    )
    subject_major = models.CharField(max_length=255)
    subject_minor = models.CharField(max_length=255)
    target_test = models.CharField(max_length=255)
    target_grade = models.CharField(max_length=255)
    track_name = models.CharField(max_length=255)
    book = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    link = models.CharField(max_length=255, blank=True)
    followers = models.ManyToManyField('User', blank =True)
    followers_num = models.IntegerField()
    #comment_track = models.ManyToManyField('Comment_Track', blank=True)
    rating_avg = models.DecimalField(max_digits=5, decimal_places=2)
    #task = models.ManyToManyField('Task')
    tags = models.ManyToManyField('Tag')
    ingredients = models.ManyToManyField('Ingredient')
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)
    published_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Task(models.Model):
    order_major = models.CharField(max_length=255)
    order_minor = models.CharField(max_length=255)
    task_name = models.CharField(max_length=255)
    ranges = models.CharField(max_length=255)
    learning_time = models.CharField(max_length=255)
    guideline = models.CharField(max_length=255)
    #comment_task = models.CharField(max_length=255)
    references = models.CharField(max_length=255)


class Recipe(models.Model):
    """Recipe object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField('Tag')
    ingredients = models.ManyToManyField('Ingredient')
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title

class Tag(models.Model):
    """Tag for filtering recipes."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient for recipes."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
