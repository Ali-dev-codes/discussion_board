from django.contrib import admin
from .models import Board, Topic, Post
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.models import Group

admin.site.site_header = "Board Admin Panel"
admin.site.site_title = "Board Admin Panel"


class TopicAdmin(ImportExportModelAdmin):  # ← هنا الدمج!
    fields = ('subject', 'board', 'created_by', 'views')
    list_display = ('subject', 'board', 'created_by', 'combine_subject_and_board')
    list_display_links = ('board', 'created_by')
    list_editable = ('subject',)
    list_filter = ('created_by', 'board')
    search_fields = [
        'subject',
        'board__name',
        'created_by__username',
    ]

    def combine_subject_and_board(self, obj):
        return f"{obj.subject} - {obj.board}"


admin.site.register(Topic, TopicAdmin)  # ← تسجيل واحد فقط

admin.site.register(Board)
admin.site.register(Post)
