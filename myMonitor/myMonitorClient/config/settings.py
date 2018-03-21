#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-

configs ={
    'HostID': 1,
    "Server": "localhost",
    "ServerPort": 8080,
    "urls":{
        'get_configs' :['api/client/config','get'],  #acquire all the services will be monitored
        'service_report': ['api/client/service/report/','post'],
    },
    'RequestTimeout':30,
    'ConfigUpdateInterval': 10, #5 mins as default

}