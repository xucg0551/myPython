from django.shortcuts import render, HttpResponse
import json
from monitor.serializer import ClientHandler

# Create your views here.

def client_configs(request, client_id):
    config_obj = ClientHandler(client_id)
    config = config_obj.fetch_configs()
    if config:
        print(json.dumps(config))
        return HttpResponse(json.dumps(config))
