from django.db import models

class Poter(models.Model):
    title = models.CharField(max_length=60)
