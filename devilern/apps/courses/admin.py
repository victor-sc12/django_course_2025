from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)} 
    list_display = ('title', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'categories__name')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')
    search_fields = ('name',)

@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ('course__title', 'category__name',)
    list_filter = ('category',)
    search_fields = ('course__title',)

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course__title',)
    list_filter = ('course__title',)
    search_fields = ('title', 'course__title',)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course__title', 'enrolled_at')
    list_filter = ('user', 'course__title', 'enrolled_at')
    search_fields = ('user', 'course__title')

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'course__title', 'status', 'progress')
    list_filter = ('user', 'course__title', 'status')
    search_fields = ('user', 'course__title', 'status')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'course__title', 'rating', 'created_at')
    list_filter = ('rating', 'course__title', 'created_at')
    search_fields = ('user', 'course__title', 'comment')


# Content Model y parent models register:
@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('module__title', 'content_type', 'item')
    list_filter = ('module__title',)

@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_display = ('owner', 'title', 'content', 'updated_at')

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('owner', 'title', 'url', 'updated_at')

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('owner', 'title', 'file', 'updated_at')

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('owner', 'title', 'file', 'updated_at')