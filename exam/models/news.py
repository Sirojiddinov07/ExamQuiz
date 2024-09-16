from  django.db import models
from django.utils.translation import gettext_lazy as _

from exam.models import AbstractBaseModel


class News(AbstractBaseModel):
    image = models.ImageField(upload_to="news_images")
    title = models.CharField(max_length=200)
    text = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("News")
        verbose_name_plural = _("News")
