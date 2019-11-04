from django.db import models

# Create your models here.


class EmailSubscribe(models.Model):
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
