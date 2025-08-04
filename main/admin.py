
from django.contrib import admin
from .models import  User, Topic, Entry

# Register your models here.

admin.site.register(User)
admin.site.register(Topic)
admin.site.register(Entry)
