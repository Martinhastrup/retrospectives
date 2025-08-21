from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import Team, Retrospective, RetrospectiveItem, ActionItem

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'userfullname', 'role', 'is_active', ]
    search_fields = ['email', 'userfullname', 'role']
    ordering = ['-email']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('userfullname',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('userfullname',)}),
    )


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name', 'description']
    filter_horizontal = ['members']
    ordering = ['-created_at']


@admin.register(Retrospective)
class RetrospectiveAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'description']
    ordering = ['-created_at']


@admin.register(RetrospectiveItem)
class RetrospectiveItemAdmin(admin.ModelAdmin):
    list_display = ['category', 'content', 'retrospective', 'author', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['content', 'retrospective__title']
    ordering = ['-created_at']


@admin.register(ActionItem)
class ActionItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'retrospective', 'assigned_to', 'status', 'priority', 'due_date']
    list_filter = ['status', 'priority', 'due_date']
    search_fields = ['title', 'description']
    ordering = ['-created_at'] 