from django.db import models

# Create your models here.


class website(models.Model):
    name = models.CharField("名称", max_length=50)
    url = models.URLField("网址")

    def __str__(self):
        return self.name