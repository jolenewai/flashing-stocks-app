from django.contrib import admin
from .models import Tag, Category, Photo

# Register your models here.
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Photo)
