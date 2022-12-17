from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'complete',
                    'colors', 'created_at', 'updated_at', 'pk')
    list_display_links = ('user', 'title')
    search_fields = ('title', 'user')
    list_filter = ('created_at', 'updated_at', 'complete')
    exclude = ('description',)



admin.site.register(Task, TaskAdmin)
