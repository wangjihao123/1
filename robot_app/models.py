from django.db import models

# Create your models here.


class QA(models.Model):
    question = models.CharField(max_length=30, verbose_name='问题')
    answer = models.TextField(verbose_name='答案')
