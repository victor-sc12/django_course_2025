from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Autor(models.Model):
    name = models.CharField(max_length=200)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

class Genero(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Libro(models.Model):
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=50, unique=True)
    publication_date = models.DateField(blank=True, null=True)
    pages = models.IntegerField(blank=True, null=True)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='libros')
    generos = models.ManyToManyField(Genero, related_name='libros')
    recomendaciones = models.ManyToManyField(get_user_model(), through='Recomendacion', verbose_name='recomendaciones')

    class Meta:
        verbose_name = 'Libro'
        verbose_name_plural = 'Libros'

    def __str__(self):
        return self.title
    
class DetalleLibro(models.Model):
    summary = models.TextField()
    cover_url = models.CharField()
    lenguage = models.CharField()
    libro = models.OneToOneField(Libro, on_delete=models.CASCADE, related_name='detalle')

class Review(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='reviews_libro')
    usuario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='reviews_usuario')
    rating = models.PositiveIntegerField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} -> {self.libro} ({self.rating}/5)" 
    
class Loan(models.Model):
    usuario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='loans_usuario')
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='loans_libro')
    loan_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.usuario} -> {self.libro} (Devuelto: {'Sí' if self.is_returned else 'No'})" 
    
class Recomendacion(models.Model):
    usuario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    recommendation_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)

    class Meta:
        unique_together = ('usuario', 'libro')