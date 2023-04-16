from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import DishType, Cook, Dish


@admin.register(DishType)
class DishTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'dish_type')
    list_filter = ('dish_type',)
    filter_horizontal = ('cooks',)
    search_fields = ('name', 'description')


@admin.register(Cook)
class CookAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Cook fields', {'fields': ('years_of_experience',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Cook fields', {'fields': ('first_name', 'last_name', 'years_of_experience',)}),
    )
    list_display = (
        'first_name',
        'last_name',
        'username',
        'years_of_experience',
        'is_staff',
        'is_superuser'
    )
    list_filter = ('is_staff', 'is_superuser', 'years_of_experience')
    search_fields = (
        'first_name',
        'last_name',
        'username',
        'years_of_experience'
    )
    ordering = ('username',)


admin.site.unregister(Group)
