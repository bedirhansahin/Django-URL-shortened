from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator
from django.utils import timezone
from django.utils.text import slugify

import random
import string


# Creating URL model
class URLData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    url = models.CharField(
        max_length=255,
        validators=[
            URLValidator(message="Lütfen Geçerli Bir URL girin. (ex: https://example.com)")
        ],
    )
    shortened_url = models.CharField(max_length=10, unique=True, blank=True)
    click_count = models.PositiveIntegerField(default=0, editable=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    last_click_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.shortened_url

    def increment_click_count(self):
        self.click_count += 1
        self.save()

    def save(self, *args, **kwargs):
        if not self.shortened_url:
            self.shortened_url = "".join(
                random.choices(string.ascii_letters, k=random.randint(3, 8))
            )

        self.shortened_url = slugify(self.shortened_url)

        super().save(*args, **kwargs)
