from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Achievement, UserAchievement

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'level', 'xp', 'is_email_verified', 'date_joined']
    list_filter = ['is_email_verified', 'is_staff', 'is_active']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Profile', {'fields': ('display_name', 'bio', 'avatar', 'xp', 'level', 'is_email_verified')}),
    )

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['name', 'rarity', 'xp_reward']
    list_filter = ['rarity']
