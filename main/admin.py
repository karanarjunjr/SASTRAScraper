from django.contrib import admin
from .models import ListItem, Recepient
# Register your models here.
admin.site.register(Recepient)
admin.site.register(ListItem)