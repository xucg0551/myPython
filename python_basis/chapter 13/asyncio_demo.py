#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-

import aiohttp
import asyncio
# from aiohttp.errors import ProxyConnectionError, ServerDisconnectedError, ClientResponseError, ClientConnectionError


# @asyncio.coroutine
# def hello():
#     print('Hello world!')
#     r = yield from asyncio.sleep(5)
#     print('Hell again!')
#     print(r)
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(hello())
# loop.close()


# import threading
# @asyncio.coroutine
# def hello():
#     print('Hello world! (%s)' % threading.currentThread())
#     yield from asyncio.sleep(1)
#     print('Hello again! (%s)' % threading.currentThread())
#
# loop = asyncio.get_event_loop()
# tasks = [hello(), hello()]
# loop.run_until_complete(asyncio.wait(tasks))
# loop.close()


# @asyncio.coroutine
# def wget(host):
#     print('wget %s...' % host)
#     connect = asyncio.open_connection(host, 80)
#     reader, writer = yield from connect
#     header = 'GET / HTTP/1.0\r\nHost: %s\r\n\r\n' % host
#     writer.write(header.encode('utf-8'))
#     yield from writer.drain()
#     while True:
#         line = yield from reader.readline()
#         if line == b'\r\n':
#             break
#         print('%s header > %s' % (host, line.decode('utf-8').rstrip()))
#     # Ignore the body, close the socket
#     writer.close()
#
# loop = asyncio.get_event_loop()
# tasks = [wget(host) for host in ['www.sina.com.cn', 'www.sohu.com', 'www.163.com']]
# loop.run_until_complete(asyncio.wait(tasks))
# loop.close()

# async def hello():
#     print('Hello world!')
#     r = await asyncio.sleep(1)
#     print('Hello again')
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(hello())
# loop.close()

async def test_single_proxy(proxy):
    """
    text one proxy, if valid, put them to usable_proxies.
    """
    try:
        async with aiohttp.ClientSession() as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                print('Testing', proxy )
                # self._conn.put(proxy)

                proxies = {
                    "http": "http://120.205.70.102:8060",
                    "https": "https://120.205.70.102:8060",
                }

                async with session.get(url='http://www.ifeng.com/', proxy=real_proxy) as response:
                    if response.status == 200:
                        # self._conn.put(proxy)
                        print('Valid proxy', proxy)
            except Exception as e:
                print('Invalid proxy', proxy)
    except Exception as s:
        print(s)
        pass


def test():
    """
    aio test all proxies.
    """
    print('ValidityTester is working')
    try:
        loop = asyncio.get_event_loop()
        tasks = [test_single_proxy(proxy) for proxy in ['120.205.70.102:8060']]
        loop.run_until_complete(asyncio.wait(tasks))
    except ValueError:
        print('Async Error')

test()
print('霜期fsafsadfafa')
