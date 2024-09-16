from django.db import models
from django.utils.translation import gettext_lazy as _
from exam.models.models import AbstractBaseModel


class Question(AbstractBaseModel):

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        ordering = ['id']



    question_number = models.CharField(max_length=4)
    title =models.TextField()


    def __str__(self):
        return self.title
