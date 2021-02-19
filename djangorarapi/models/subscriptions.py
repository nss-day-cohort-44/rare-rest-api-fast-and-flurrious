from django.db import models


class Subscription(models.Model):

            follower = models.ForeignKey("Rareuser", on_delete=models.CASCADE)
            author = models.ForeignKey("Rareuser", on_delete=models.CASCADE)
            created_on = models.DateField(auto_now=False, auto_now_add=False)
            ended_on = models.DateField(auto_now=False, auto_now_add=False)