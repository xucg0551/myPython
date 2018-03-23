from django.shortcuts import render, HttpResponse
import json
from monitor.serializer import ClientHandler
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def client_configs(request, client_id):
    config_obj = ClientHandler(client_id)
    config = config_obj.fetch_configs()
    if config:
        print(json.dumps(config))
        return HttpResponse(json.dumps(config))



@csrf_exempt
def service_data_report(request):
    if request.method == 'POST':
        print("---->",request.POST)
        #REDIS_OBJ.set("test_alex",'hahaha')
        # try:
        #     print('host=%s, service=%s' %(request.POST.get('client_id'),request.POST.get('service_name') ) )
        #     data =  json.loads(request.POST['data'])
        #     #print(data)
        #     #StatusData_1_memory_latest
        #     client_id = request.POST.get('client_id')
        #     service_name = request.POST.get('service_name')
        #     #把数据存下来
        #     data_saveing_obj = data_optimization.DataStore(client_id,service_name,data,REDIS_OBJ)
        #
        #     #redis_key_format = "StatusData_%s_%s_latest" %(client_id,service_name)
        #     #data['report_time'] = time.time()
        #     #REDIS_OBJ.lpush(redis_key_format,json.dumps(data))
        #
        #     #在这里同时触发监控(在这里触发的好处是什么呢？)
        #     host_obj = models.Host.objects.get(id=client_id)
        #     service_triggers = get_host_triggers(host_obj)
        #
        #     trigger_handler = data_processing.DataHandler(settings,connect_redis=False)
        #     for trigger in service_triggers:
        #         trigger_handler.load_service_data_and_calulating(host_obj,trigger,REDIS_OBJ)
        #     print("service trigger::",service_triggers)
        #
        #
        #     #更新主机存活状态
        #     #host_alive_key = "HostAliveFlag_%s" % client_id
        #     #REDIS_OBJ.set(host_alive_key,time.time())
        # except IndexError as e:
        #     print('----->err:',e)


    return HttpResponse(json.dumps("---report success---"))
