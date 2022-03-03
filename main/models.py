from django.db import models
# Create your models here.

class Recepient(models.Model):
    Email = models.CharField(max_length=500)

# class ListManager(models.Manager):
#     def create_obj(self, title, link):
#         listItem = self.create(title=title, link=link)
#         return listItem

class ListItem(models.Model):
    title = models.CharField(max_length=500)
    link = models.CharField(max_length=1000)

    # objects = ListManager()