from django.db import models

# Create your models here.
class Autor(models.Model):
    name = models.CharField(max_length=200)
    birth_date = models.DateField(blank=True, null=True)


class Libro(models.Model):
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=50, unique=True)
    publication_date = models.DateField(blank=True, null=True)
    pages = models.IntegerField(blank=True, null=True)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='libros')