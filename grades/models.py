from django.db import models

# Create your models here.

class Grade(models.Model):
    grade = models.IntegerField(unique=True, blank=False, null=False)

    def __str__(self):
        return str(self.grade)