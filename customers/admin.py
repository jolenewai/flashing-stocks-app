from django.contrib import admin
from .models import Customer, Download, Favourite


# Register your models here.


admin.site.register(Customer)
admin.site.register(Download)
admin.site.register(Favourite)
