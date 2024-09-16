from django.db import models
from django.utils.translation import gettext_lazy as _

from datetime import timedelta

from exam.models.category import Category


class Quizzes(models.Model):


    class Meta:
        verbose_name = _("Quiz")
        verbose_name_plural = _("Quizzes")
        ordering = ['id']

    title = models.CharField(max_length=255, default=_(
        "New Quiz"), verbose_name=_("Quiz Title"))
    category = models.ForeignKey(
        Category,  on_delete=models.DO_NOTHING)
    date_created = models.DateTimeField(auto_now_add=True)
    questions = models.ManyToManyField("Question")
    duration = models.DurationField(default=timedelta(minutes=60))
    is_free = models.BooleanField(default=False)
    def __str__(self):
        return self.title