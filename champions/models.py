from django.db import models

from django.db import models

class Champion(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=50, blank=True, null=True)
    strong_against = models.ManyToManyField('self', related_name='weak_against_me', symmetrical=False, blank=True)
    weak_against = models.ManyToManyField('self', related_name='strong_against_me', symmetrical=False, blank=True)

    def __str__(self):
        return self.name
