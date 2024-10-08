from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from PIL import Image
from authentication.models import User


class Ticket(models.Model):
    """ Ticket model class"""
    # Your Ticket model definition goes here
    title = models.CharField(max_length=120)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    IMAGE_MAX_SIZE = (258, 392)

    def resize_image(self):
        """ Method to resize an image before saving"""
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        """ Method save overridden"""
        super().save(*args, **kwargs)
        self.resize_image()


class Review(models.Model):
    """ Review model class"""
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        # validates that rating must be between 0 and 5
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)


class UserFollows(models.Model):
    """ Userfollows model class"""
    # Your UserFollows model definition goes here
    following_user = models.ForeignKey(
                    to=settings.AUTH_USER_MODEL,
                    on_delete=models.CASCADE,
                    related_name='following')
    followed_user = models.ForeignKey(
                    to=settings.AUTH_USER_MODEL,
                    on_delete=models.CASCADE,
                    related_name='followers')
    class Meta:
        """meta class"""
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = ('following_user', 'followed_user')
