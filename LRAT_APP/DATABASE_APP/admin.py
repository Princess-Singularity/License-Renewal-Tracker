from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Software, SoftwareOption, Subscription
# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("group_names",)
    search_fields = ("username", "email", "first_name", "last_name")
    list_filter = ("groups", "is_staff", "is_superuser", "is_active")
    ordering = ("last_name",)

    @admin.display(description="Groups")
    def group_names(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])

admin.site.register(Software)
admin.site.register(SoftwareOption)
admin.site.register(Subscription)
