from django.db import models


class Reaction(models.Model):

            label = models.CharField(max_length=50)
            image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None)