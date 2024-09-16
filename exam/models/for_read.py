from django.db import models

from exam.models.models import AbstractBaseModel


class ForRead(AbstractBaseModel):
    title = models.CharField(max_length=150)
    text = models.TextField()
    image = models.ImageField(upload_to="for_read_image/", null=True, blank=True)

    def __str__(self):
        return self.title