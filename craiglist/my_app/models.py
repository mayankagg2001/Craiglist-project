from django.db import models
from django.utils import timezone
class Search(models.Model):
    search = models.CharField(max_length=100)
    created = models.DateTimeField(default = timezone.now())
    def __str__(self):
        return self.search
    class Meta:
        verbose_name = 'search'
        verbose_name_plural = 'Searches'