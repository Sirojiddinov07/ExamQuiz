from django.db import models
from exam.models.question import Question
from exam.models.for_read import ForRead
from exam.models.models import AbstractBaseModel


class Addition(AbstractBaseModel):
    image = models.ImageField(upload_to="addition_image/", null=True, blank=True)
    text = models.ForeignKey(ForRead, on_delete=models.CASCADE, null=True, blank=True)
    questions = models.ManyToManyField(Question)
