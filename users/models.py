from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image


class User(AbstractUser):
    image = models.ImageField(default='default.jpg', upload_to='user_images')

    def save(self, *args, **kwargs):
        """Overwrite save method to resize every profile image"""
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 128 or img.width > 128:
            output_size = (128, 128)
            img.thumbnail(output_size)
            img.save(self.image.path)
