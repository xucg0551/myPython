from django.contrib import admin
from monitor import models

# Register your models here.


class HostAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'ip_addr', 'status')
    filter_horizontal = ('templates', 'host_groups')

class HostGroupAdmin(admin.ModelAdmin):
    filter_horizontal = ('templates', )

class TemplateAdmin(admin.ModelAdmin):
    filter_horizontal = ('services',)

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'interval', 'plugin_name')




admin.site.register(models.Host, HostAdmin)
admin.site.register(models.HostGroup, HostGroupAdmin)
admin.site.register(models.Template, TemplateAdmin)
admin.site.register(models.Service, ServiceAdmin)
