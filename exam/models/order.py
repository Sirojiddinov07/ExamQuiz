from django.contrib.auth.models import User
from django.db import models

from exam.models import Category


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    total_price = models.DecimalField(max_digits=30, decimal_places=2, default=0.00)
    start_day = models.DateField(null=True, blank=True)
    end_day = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


 