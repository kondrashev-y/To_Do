from django.db import models
from django.utils.text import slugify


def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug


class Task(models.Model):
    """Модель задачи"""
    title = models.CharField(max_length=200, verbose_name='Задача')
    text = models.TextField()
    completed = models.BooleanField(default=False, verbose_name='Выполнен')
    finish_date = models.DateTimeField(verbose_name='Дата выполнения')
    created_date = models.DateTimeField(auto_now=True, verbose_name='Дата создания')
    change_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата изменения')
    tag = models.ManyToManyField('Tag', blank=True, related_name='tasks')

    def __str__(self):
        return self.title


class Tag(models.Model):
    """Модель тегов"""
    name = models.CharField(max_length=50, verbose_name='Тег')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

