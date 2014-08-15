from django.db import models


class User(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return u'{0}'.format(self.name)


class Team(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return u'{0}'.format(self.name)


class Message(models.Model):
    text = models.TextField()

    def __unicode__(self):
        return u'a message'


class Board(models.Model):
    name = models.CharField(max_length=64)

    def __unicode__(self):
        return u'{0}'.format(self.name)
