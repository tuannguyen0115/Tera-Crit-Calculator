# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Boss(models.Model):
    name = models.CharField(max_length=255)
    level_diff = models.IntegerField()
    mobtype = models.IntegerField()
    cr = models.IntegerField()
    def __repr__(self):
        return "<Boss Object: {} >".format(self.name)

class Class(models.Model):
    name = models.CharField(max_length=255)
    base_cf = models.IntegerField()
    def __repr__(self):
        return "<Class Object: {} >".format(self.name)    

class Skill(models.Model):
    name = models.CharField(max_length=255)
    g = models.FloatField()
    i = models.FloatField()
    b = models.FloatField()
    a = models.FloatField()
    of_class = models.ForeignKey(Class, related_name="classes")
    def __repr__(self):
        return "<Skill Object: {} >".format(self.name) 
    