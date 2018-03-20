#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
print(datetime.now())

#datetime--->timestamp
dt = datetime(2018, 3, 7, 2, 54) #指定日期时间创建datetime
print(dt)
print(dt.timestamp())  # 把datetime转换为timestamp

#timestamp--->datetime
t = 1429417200.0
print(datetime.fromtimestamp(t))

#str--->datetime
cday = datetime.strptime('2018-3-7 3:1:59', '%Y-%m-%d %H:%M:%S')
print(cday)

#datetime--->str
now = datetime.now()
print(now.strftime('%a, %b %d %H:%M'))
print(now.strftime('%Y/%m/%d'))

#datetime  timedelta
now = datetime.now()
print(now + timedelta(hours=-1))
print(now + timedelta(days=-1, hours=-1))