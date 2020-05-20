from django.db import models
from photographers.models import Photographer, Album


class Tag(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Photo(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    desc = models.CharField(max_length=255, blank=False, null=False)
    url = models.URLField(blank=False)
    costs = models.FloatField(blank=False)
    tags = models.ManyToManyField('Tag')
    category = models.ManyToManyField('Category')
    owner = models.ForeignKey(
        Photographer,
        on_delete='CASCADE'
    )
    # album = models.ManyToManyField(Album)

    def __str__(self):
        return self.id + '_' + self.title
