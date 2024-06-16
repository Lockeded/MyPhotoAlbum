from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name


class Photo(models.Model):
    class Meta:
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'
    
    image = models.ImageField(upload_to='photos/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='photos')
    save_to_original_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='original_photos', null=True, blank=True)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.description
