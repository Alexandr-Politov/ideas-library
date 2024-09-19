from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import Idea, User, Category, Comment


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("occupation",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("occupation",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "occupation",
                    )
                },
            ),
        )
    )


@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = ("categories",)
    list_display = ("name", "difficulty", "author")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    search_fields = ("author",)
    list_filter = ("author",)


admin.site.register(Category)
admin.site.unregister(Group)
