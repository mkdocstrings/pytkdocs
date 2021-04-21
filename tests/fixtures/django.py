from django import setup
from django.conf import settings
from django.db import models

settings.configure()
setup()


class Person(models.Model):
    """Simple Django Model for a person's information"""
    name = models.CharField(verbose_name='Name')
    age = models.IntegerField(verbose_name='Age')
    parent = models.ForeignKey(verbose_name='Parent', to='Child', on_delete=models.CASCADE)

    class Meta:
        app_label = 'django'


class Child(models.Model):
    name: str = models.CharField(verbose_name='Name')

    class Meta:
        app_label = 'django'
