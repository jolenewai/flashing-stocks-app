from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name