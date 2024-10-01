from django.db import models
from grades.models import Grade
from teachers.models import Teacher

# Create your models here.


class Class(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False, unique=True)
    subject = models.CharField(max_length=128, blank=False, null=False)
    teacher = models.ForeignKey(Teacher, models.PROTECT)
    class_code = models.CharField(max_length=64, blank=False, null=False)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, blank=False, null=False)
    time_table = models.JSONField(blank=True, null=True, verbose_name="Time Table")

    def _make_code(self):
        return self.subject[0:3].upper() + str(self.grade)


    def save(self, *args, **kwargs):
        self.class_code = self._make_code()
        super().save(*args, **kwargs)

