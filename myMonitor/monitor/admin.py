from django.contrib import admin
from monitor import models

# Register your models here.


class HostAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'ip_addr', 'status')







admin.site.register(models.Host, HostAdmin)
