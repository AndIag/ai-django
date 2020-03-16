import logging
from datetime import datetime

from django.db import models
from django.db.models import QuerySet

from ai_django.ai_core.utils.shortcuts import all_none, today

logger = logging.getLogger(__name__)


class DatableQuerySet(QuerySet):
    """Adds .schedule() method to QuerySet allowing quick filter by (date, day, week, month and year)"""
    def schedule(self, **kwargs):
        params = {}
        date = kwargs.pop('date', None)
        day = kwargs.pop('day', None)
        week = kwargs.pop('week', None)
        month = kwargs.pop('month', None)
        year = kwargs.pop('year', None)

        if all_none(date, day, week, month, year):
            # Default to current week
            week, year = today()[1], today()[0]

        if date:
            params[self.model.schedule_by] = date.date() if isinstance(date, datetime) else date
        if day:
            params["{}__day".format(self.model.schedule_by)] = day
        if week:
            params["{}__week".format(self.model.schedule_by)] = week
        if month:
            params["{}__month".format(self.model.schedule_by)] = month
        if year:
            params["{}__year".format(self.model.schedule_by)] = year

        return self.filter(**params)


class DatableManager(models.Manager):
    """Adds .schedule() method to Manager allowing quick filter by (date, day, week, month and year)"""
    def get_queryset(self):
        return DatableQuerySet(self.model, using=self._db)

    def schedule(self, **kwargs):
        return self.get_queryset().schedule(**kwargs)


class DatableModel(models.Model):
    """Set DatableManager as model manager allowing quick filter by (date, day, week, month and year)"""

    schedule_by = None
    objects = DatableManager()

    class Meta:
        abstract = True
