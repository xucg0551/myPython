#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist
from . import models

class ClientHandler(object):
    def __init__(self, client_id):
        self.client_id = client_id
        self.client_configs = {
            'services':{

            }
        }

    def fetch_configs(self):
        try:
            host_obj = models.Host.objects.get(id = self.client_id)
            template_list = list(host_obj.templates.select_related())  # templates = list(host_obj.templates.all())
            for host_group in host_obj.host_groups.select_related():
                template_list.extend(host_group.templates.select_related())
            print(template_list)

            for template in template_list:
                for service in template.services.select_related():
                    print(service)
                    self.client_configs['services'][service.name] = [service.plugin_name, service.interval]
        except ObjectDoesNotExist as e:
            pass
        return self.client_configs
