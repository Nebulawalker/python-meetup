from django.contrib import admin

from .models import Report, Issue, ChatState


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    readonly_fields = [
        'id',
    ]

    list_display = [
        'speaker',
        'topic',
        'starts_at',
        'ends_at',
        'is_current',
    ]

    ordering = ['starts_at']


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    readonly_fields = [
        'id',
    ]

    list_display = [
        'from_whom',
        'report',
        'status',
    ]

    ordering = ['asked_at']


@admin.register(ChatState)
class ChatStateAdmin(admin.ModelAdmin):
    list_display = [
        'chat_id',
        'state',
        'modified_at',
    ]
    readonly_fields = ['created_at', 'modified_at']
    ordering = ['-modified_at']
