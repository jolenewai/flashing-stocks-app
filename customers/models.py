from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import User


class Person(models.Model):

    user = models.OneToOneField(User, on_delete='CASCADE')
    display_name = models.CharField(max_length=100, blank=False, null=False)
    dob = models.DateField(auto_now=False)
    profile_img = models.URLField()
    join_date = models.DateField(auto_now_add=True)
    address_line1 = models.CharField(max_length=100, blank=True)
    address_line2 = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50, blank=True)
    country = CountryField()
    country_code = models.IntegerField()
    contact_number = models.IntegerField()

    class Meta:
        abstract = True


class Customer(Person):
    pass

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name + ' (' + self.display_name + ')'

