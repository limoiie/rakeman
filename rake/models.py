from django.db import models


class QueryResultItem(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField()
    digest = models.CharField(max_length=300)
    keywords = models.CharField(max_length=100)
    source = models.CharField(max_length=50)
    datetime = models.DateTimeField()
