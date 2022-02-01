
from django.db import models
from django.urls import reverse
from django.conf import settings
# Create your models here.
import misaka
from categories.models import Category

from django.contrib.auth import get_user_model
User = get_user_model()

class Movie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='movies')
    name = models.TextField()
    name_html = models.TextField(editable = False)
    release = models.DateField(blank=True)
    category = models.ForeignKey(Category, related_name='movies', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.name_html = misaka.html(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("movies:single", kwargs={"username": self.user.username,'pk':self.pk})
    
    class Meta:
        ordering = ['-release']
        unique_together = ['user', 'name']
