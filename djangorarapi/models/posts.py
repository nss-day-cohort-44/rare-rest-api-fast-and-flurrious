from django.db import models


class Post(models.Model):

            user = models.ForeignKey("Rareuser", on_delete=models.CASCADE)
            category = models.ForeignKey("Category", on_delete=models.SET_NULL)
            title = models.CharField(max_length=200)
            publication_date = models.DateField(auto_now=False, auto_now_add=False)
            profile_image_url = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None)
            content = models.CharField(max_length=1500)
            approved = models.BooleanField()