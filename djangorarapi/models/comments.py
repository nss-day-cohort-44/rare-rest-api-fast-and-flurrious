from django.db import models


class Comment(models.Model):

            post = models.ForeignKey("Post", on_delete=models.CASCADE)
            author = models.ForeignKey("Rareuser", on_delete=models.CASCADE)
            content = models.CharField(max_length=280)
            created_on = models.DateTimeField(auto_now=True, auto_now_add=False)