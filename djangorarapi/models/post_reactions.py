from django.db import models


class Post_Reaction(models.Model):

            reaction = models.ForeignKey("Reaction", on_delete=models.CASCADE)
            post = models.ForeignKey("Post", on_delete=models.CASCADE)