from django.contrib import admin
from .models import CustomUser, Software, SoftwareOption, Subscription
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Software)
admin.site.register(SoftwareOption)
admin.site.register(Subscription)
