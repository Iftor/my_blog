from django.contrib import admin
from . import models


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'registration_date')


@admin.register(models.Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')


@admin.register(models.BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'blog', 'pub_date', 'delete_date')
    exclude = ('delete_date',)
