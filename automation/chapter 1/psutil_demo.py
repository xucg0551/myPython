import psutil


#memory
mem = psutil.virtual_memory()
print(mem)
print(psutil.swap_memory())

#cpu
print(psutil.cpu_times())
print(psutil.cpu_count())
print(psutil.cpu_count(logical=False))
print(psutil.cpu_times().user)

#disk
print(psutil.disk_partitions())
print(psutil.disk_usage('/'))