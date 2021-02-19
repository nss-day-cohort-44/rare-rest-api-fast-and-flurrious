from django.db import models


class Demotionqueue(models.Model):

            action = models.CharField(max_length=150)
            admin = models.ForeignKey("Rareuser", on_delete=models.CASCADE)
            approver_one = models.ForeignKey("Rareuser", on_delete=models.CASCADE)