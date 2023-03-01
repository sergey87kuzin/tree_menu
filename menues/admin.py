from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Menu


class MenuAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'parent')
    search_fields = ('slug', 'name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(Menu, MenuAdmin)
admin.site.unregister(Group)
