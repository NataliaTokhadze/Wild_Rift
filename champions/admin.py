from django.contrib import admin
from .models import Champion

@admin.register(Champion)
class ChampionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'role')  
    search_fields = ('name', 'role')
    list_filter = ('role',) 
    ordering = ('id',)
