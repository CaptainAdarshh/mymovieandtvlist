from django.db import models
from django.utils.text import slugify
from django.urls import reverse
# Create your models here.
import misaka

from django.contrib.auth import get_user_model
User = get_user_model()


from django import template
register = template.Library()

class Category(models.Model):
    name = models.CharField(max_length=500, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super.save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("category:single", kwargs={"slug": self.slug})
    
    
