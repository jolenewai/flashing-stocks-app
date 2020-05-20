from django.db import models
from customers.models import Person


class Photographer(Person):

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name + ' (' + self.display_name + ')'


class Album(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    desc = models.CharField(max_length=255, blank=False, null=False)
    tags = models.ManyToManyField('photos.Tag')
    category = models.ManyToManyField('photos.Category')
    owner = models.ForeignKey(Photographer, on_delete='CASCADE')

    def __str__(self):
        return self.title

