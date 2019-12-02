from django.contrib import admin

from .models import Project, Member, TaskKind, Task, Milestone, TaskLink

admin.site.register(
    Project,
    list_display=[
        "fullname",
        "active_flag",
        "private_type",
        "created_at",
        "created_user",
        "modified_at",
        "modified_user",
    ],)

admin.site.register(
    Member,
    list_display=[
        "member_profile",
        "project",
        "admin_flag",
        ]
    )

admin.site.register(
    TaskKind,
    list_display=[
        "name",
        ]
    )

admin.site.register(
    Task,
    list_display=[
        "fullname",
        "project",
        "created_at",
        "created_user",
        "modified_at",
        "modified_user",
        "finished_fact_at",
        "important",
        ]
    )

admin.site.register(
    Milestone,
    )

admin.site.register(
    TaskLink,
    list_display=[
        "maintask",
        "subtask",
    ], )
