from django.contrib.contenttypes.models import ContentType
from django.db import models
from entity.models import Entity


class Subscription(models.Model):
    medium = models.ForeignKey('Medium')
    source = models.ForeignKey('Source')
    entity = models.ForeignKey(Entity)
    subentity_type = models.ForeignKey(ContentType)


class Unsubscribe(models.Model):
    entity = models.ForeignKey(Entity)
    medium = models.ForeignKey('Medium')
    source = models.ForeignKey('Source')


class Medium(models.Model):
    name = models.CharField(max_length=64, unique=True)
    display_name = models.CharField(max_length=64)
    description = models.TextField()


class Source(models.Model):
    name = models.CharField(max_length=64, unique=True)
    display_name = models.CharField(max_length=64)
    description = models.TextField()
