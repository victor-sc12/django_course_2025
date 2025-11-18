from django.db import models
from .course import Course
from ..fields import OrderField

class Module(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='curso_modulos')
    order = OrderField(blank=True, for_fields = ['course'])

    def __str__(self):
        return f'{self.course.title} -- {self.title}'