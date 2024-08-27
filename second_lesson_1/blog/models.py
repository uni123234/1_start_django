from django.db import models
from django.utils import timezone


class Post(models.Model):
    title = models.CharField(max_length=60)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='posts', null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-publish']


class Category(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


