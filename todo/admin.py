from django.contrib import admin
from .models import Todo


#to show the created date in databases
class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)



admin.site.register(Todo, TodoAdmin)
