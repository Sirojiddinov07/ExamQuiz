from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=30, decimal_places=2)

    def __str__(self):
        return self.name
