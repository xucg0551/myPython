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
            print(host_obj)
            return 1024
        except ObjectDoesNotExist as e:
            pass
        return self.client_configs
