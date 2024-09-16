from django.contrib.auth.models import User
from django.db import models

from django.utils.translation import gettext_lazy as _

from exam.models import Quizzes


class Commentary(models.Model):
    quiz = models.ForeignKey(Quizzes, related_name='commentaries', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='commentaries', on_delete=models.CASCADE)
    text = models.TextField(verbose_name=_("Commentary"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def save(self, *args, **kwargs):
        if not self.pk and not Commentary.objects.filter(quiz=self.quiz).exists():
            self.text = "follow rules"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.text[:50]
