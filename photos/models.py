from django.db import models
from photographers.models import Photographer, Album
from pyuploadcare.dj.models import ImageField


class Tag(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.name


class Photo(models.Model):
    image = ImageField(blank=True, verbose_name="")
    date_added = models.DateField(auto_now_add=True)
    caption = models.CharField(max_length=100, blank=False, null=False)
    desc = models.CharField(max_length=255, blank=False, null=False, verbose_name="Description")
    price = models.FloatField(blank=False)
    tags = models.ManyToManyField(Tag, blank=True)
    category = models.ManyToManyField(Category, blank=True)
    owner = models.ForeignKey(
        Photographer,
        on_delete='CASCADE'
    )
    album = models.ManyToManyField(Album, blank=True)

    def __str__(self):
        return str(self.id) + '_' + self.caption
