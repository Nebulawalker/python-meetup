from django.contrib import admin

from django.contrib.auth import get_user_model


@admin.register(get_user_model())
class UserADmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'tg_id', ]
    readonly_fields = ['id']
