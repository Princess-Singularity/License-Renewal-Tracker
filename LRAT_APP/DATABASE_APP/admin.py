from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Software, SoftwareOption, Subscription
# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("is_active", "group_names",)
    search_fields = ("username", "email", "first_name", "last_name")
    list_filter = ("groups", "is_staff", "is_superuser", "is_active")
    ordering = ("last_name",)

    @admin.display(description="Groups")
    def group_names(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])

class SoftwareOptionInline(admin.TabularInline):
    model = SoftwareOption
    extra = 1
    show_change_link = True
    fields = ("name", "cost", "is_active")

@admin.register(Software)
class SoftwareAdmin(admin.ModelAdmin):
    list_display = ("subscription_name", "formatted_cost", "term_display", "is_active", "license_period")
    search_fields = ("subscription_name", "description")
    list_filter = ("is_active",)
    ordering = ("subscription_name",)
    inlines = [SoftwareOptionInline]

    @admin.display(description="Cost", ordering="cost")
    def formatted_cost(self, obj):
        return f"${obj.cost:.2f}"
    
    @admin.display(description="Term", ordering="term")
    def term_display(self, obj):
        if obj.term == 1:
            return "1 month"
        return f"{obj.term} months"
    
    @admin.display(description="License Period")
    def license_period(self, obj):
        if obj.license_start and obj.license_end:
            return f"{obj.license_start:%b %d} - {obj.license_end:%b %d}"
        if obj.license_start:
            return f"Starts {obj.license_start:%b %d}"
        if obj.license_end:
            return f"Ends {obj.license_end:%b %d}"
        return "-"

admin.site.register(Subscription)
