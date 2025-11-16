from django.contrib import admin
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# personalización del django admin panel template:
admin.site.site_header = 'Soy el panel de administración. Así es :"D'
admin.site.site_title = 'Nose'
admin.site.index_title = 'A continuación una serie de secciones para gestionar objetos'

User = get_user_model()

# Acctions (personalizadas):
@admin.action(description="Marcar libros como 'devueltos'")
def mark_as_returned(modeladmin, request, queryset):
    queryset.update(is_returned = True)

@admin.action(description="Marcar libros como 'No devueltos'")
def mark_as_unreturned(modeladmin, request, queryset):
    queryset.update(is_returned = False)


# Inlines

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1

class DetalleLibroInline(admin.StackedInline):
    model = DetalleLibro
    can_delete = False
    extra = 1

class LoanInline(admin.StackedInline):
    model = Loan
    extra = 1
    verbose_name = 'Préstamo'
    verbose_name_plural = "Préstamos"


# Personalización de admin de los modelos

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    inlines = [ReviewInline, DetalleLibroInline, LoanInline]
    list_display = ('title', 'autor', 'publication_date')
    search_fields = ('title', 'autor__name')
    list_filter = ('publication_date', 'generos')
    ordering = ('-publication_date', 'title')
    date_hierarchy = 'publication_date'
    readonly_fields = ('pages',)
    fieldsets = (
        ('Info General', {
            'fields': ('title', 'autor', 'publication_date', 'generos')      
        }),
        ('Details', {
            'fields': ('isbn', 'pages',),
            'classes': ('collapse',)      
        }),
    )
    autocomplete_fields = ('autor', 'generos')

    def has_add_permission(self, request):
        return request.user.is_superuser
    
    def has_change_permission(self, request, obj = ...):
        return request.user.is_staff

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    search_fields = ('name',)

@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    search_fields = ('name',)

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'libro', 'loan_date', 'is_returned')
    readonly_fields = ('loan_date',)
    actions = [mark_as_returned, mark_as_unreturned]

class CustomUserAdmin(BaseUserAdmin):
    inlines = [LoanInline]
    list_display = ['username', 'email']


# Register your models here.
# admin.site.register(Autor)
# admin.site.register(Libro, LibroAdmin)
# admin.site.register(Genero)
# admin.site.register(Loan)


# Registro personalizado para User Model y su clase personalizada:
try:
    admin.site.unregister(User)  # deregistrar Usuario para registrarlo posteriormente junto a su clase personalizada
except admin.sites.NotRegistered:
    pass # En caso de que no se encuentre registrado de por sí, tons no hacer nada y proceder con su registro

admin.site.register(User, CustomUserAdmin)