from django import forms
from .models import *

# LISTA bad words:
BAD_WORDS = ['fuck', 'shit', 'motherfucker']

# Creación de formulario con 'Form'
class ReviewSimpleForm(forms.Form):
    rating = forms.IntegerField(min_value=1, max_value=5, widget=forms.NumberInput(attrs={
        'placeholder': 'Califca el libro del 1 al 5',
        # la siguientes clase la estamos sacando de boostrap, obvio se puede usar estilos propios
        'class': 'form-control' 
    }))
    text = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Escribe tu reseña',
        'class': 'form-control',
        'rows':4
    }))

# Creación de formulario con ModelForm:
class ReviewForm(forms.ModelForm):

    # Podemos añadir nuevos campos al form aunque estos no esten en el modelo a poblar:
    would_recommend = forms.BooleanField(required=False, label='¿Recomendarías este libro?')

    class Meta:
        model = Review
        fields = ['rating', 'text']

        # añadir widgest personalizados a los campos del ModelForm:
        widgets = {
            'rating': forms.NumberInput(attrs={
                'placeholder': 'Ingresa un calificación del 1 al 5',
                'class': 'form-control', # por si acaso esta clase 
            }),
            'text': forms.Textarea(attrs={
                'placeholder': 'Ingresa la reseña del libro',
                'class': 'form-control',
                'rows': 4,
            }),
        }

    # Validación personalizada a nivel de campo:
    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if rating < 0 or rating > 5:
            raise forms.ValidationError("El rating debe estar en un rango de 1-5")
        
        return rating
    
    # validación personalizada para evitar mala palabra:
    def clean_text(self):
        text = self.cleaned_data['text']
        for word in BAD_WORDS:
            if word in text.lower():
                raise forms.ValidationError(f'No puedes usar esa palabra en la reseña: {word}')
                
        return text

    # Validación personalizada a nivel de campo cruzados:
    def clean(self):
        cleaned_data = super().clean()
        rating = cleaned_data.get('rating')
        text = cleaned_data.get('text')

        if rating == 1 and len(text) < 10:
            raise forms.ValidationError("Si la calificación es de 1 estrella, explica a detalle la razón.")
        
    # sobreescribir el método save del modelform para agragar lógica personalizada
    def save(self, commit = True):
        review = super().save(commit=False)

        # acá agregaríamos lógica personalizada al nuevo campo 'would_recommend' por ejemplo.
        # Por esta ocasión no se hará.

        if commit:
            review.save()

        return review