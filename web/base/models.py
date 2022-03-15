from django.db import models


class Chains(models.Model):
    name = models.CharField(max_length=100)


class Places(models.Model):
    address = models.CharField(max_length=100)
    name = models.CharField(max_length=100)


class Rooms(models.Model):
    name = models.CharField(max_length=100)


class EventRuns(models.Model):
    time = models.CharField(max_length=100)


class Events(models.Model):
    title = models.CharField(max_length=100)


class EventTypes(models.Model):
    name = models.CharField(max_length=100)
