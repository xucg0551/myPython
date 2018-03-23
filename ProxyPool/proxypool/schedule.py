#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-
from multiprocessing import Process
from .settings import *
from .db import RedisClient
import time
from .getter import FreeProxyGetter
from .error import ResourceDepletionError
import aiohttp, asyncio
# from aiohttp.errors import ProxyConnectionError, ServerDisconnectedError, ClientResponseError, ClientConnectionError

class ValidityTester(object):
    test_api = TEST_API

    def __init__(self):
        self._raw_proxies = None
        self._usable_proxies = []

    def set_raw_proxies(self, proxies):
        self._raw_proxies = proxies
        self._conn = RedisClient()

    async def test_single_proxy(self, proxy):
        """
        text one proxy, if valid, put them to usable_proxies.
        """
        try:
            async with aiohttp.ClientSession() as session:
                try:
                    if isinstance(proxy, bytes):
                        proxy = proxy.decode('utf-8')
                    real_proxy = 'http://' + proxy
                    print('Testing', proxy)
                    # self._conn.put(proxy)
                    async with session.get(self.test_api, proxy=real_proxy, timeout=PROXY_TIMEOUT) as response:
                        if response.status == 200:
                            #如果代理有效，则加入redis中
                            self._conn.put(proxy)
                            print('Valid proxy', proxy)
                except Exception as e:
                    print('Invalid proxy', proxy)
                # except (ProxyConnectionError, TimeoutError, ValueError):
                #     print('Invalid proxy', proxy)
        except Exception as e:
            print('Invalid proxy', proxy)
            pass


    #异步测试
    def test(self):
        """
        aio test all proxies.
        """
        print('ValidityTester is working')
        try:
            #获取event_loop
            loop = asyncio.get_event_loop()
            #多个协程封装组一组tasks运行
            tasks = [self.test_single_proxy(proxy) for proxy in self._raw_proxies]
            loop.run_until_complete(asyncio.wait(tasks))
        except ValueError:
            print('Async Error')

class PoolAdder(object):
    """
    add proxy to pool
    """

    def __init__(self, threshold):
        self._threshold = threshold
        self._conn = RedisClient()
        self._tester = ValidityTester()
        self._crawler = FreeProxyGetter()

    def is_over_threshold(self):
        """
        judge if count is overflow.
        """
        if self._conn.queue_len >= self._threshold:
            return True
        else:
            return False

    def add_to_queue(self):
        print('PoolAdder is working')
        proxy_count = 0

        #如果当前IP有效数小于最大的阀值，则循环获取
        #获取IP后，也要进行验证(self._tester.test())，并不能直接放进redis里
        while not self.is_over_threshold():
            for callback_label in range(self._crawler.__CrawlFuncCount__):  #这里代码是精华！！！！！！，通过metaclass充分实现了设计模式中的"开闭"原则
                callback = self._crawler.__CrawlFunc__[callback_label]
                raw_proxies = self._crawler.get_raw_proxies(callback)
                # test crawled proxies
                self._tester.set_raw_proxies(raw_proxies)
                self._tester.test()
                proxy_count += len(raw_proxies)
                if self.is_over_threshold():
                    print('IP is enough, waiting to be used')
                    break
            if proxy_count == 0:
                raise ResourceDepletionError


class Schedule(object):
    @staticmethod
    def valid_proxy(cycle=VALID_CHECK_CYCLE):
        """
        Get half of proxies which in redis
        """
        #生成一个缓存对象、检测代理的对象
        conn = RedisClient()
        tester = ValidityTester()

        #循环验证，每次取一半代理进行验证
        while True:
            print('Refreshing ip')

            # 从redis里获取1/2的IP代理，并从缓存里删除已经取出来的count个代理
            count = int(0.5 * conn.queue_len)
            if count == 0:
                print('Waiting for adding')
                time.sleep(cycle)
                continue
            raw_proxies = conn.get(count)

            #进行代理的测试验证(异步验证)
            tester.set_raw_proxies(raw_proxies)
            tester.test()

            time.sleep(cycle)

    @staticmethod
    def check_pool(lower_threshold=POOL_LOWER_THRESHOLD,
                   upper_threshold=POOL_UPPER_THRESHOLD,
                   cycle=POOL_LEN_CHECK_CYCLE):
        """
        If the number of proxies less than lower_threshold, add proxy
        """
        # 生成一个缓存对象、获取代理的对象
        conn = RedisClient()
        adder = PoolAdder(upper_threshold)

        #无限循环获取代理，如果有效IP小于最小的阀值，则爬取IP代理
        while True:
            if conn.queue_len < lower_threshold:
                adder.add_to_queue()
            time.sleep(cycle)

    def run(self):
        #开辟两个进程，一个用于验证reids里的IP(因为redis里的IP也会随时失效)，另一个用于获取IP代理，对获取的IP也要进行验证
        valid_process = Process(target=Schedule.valid_proxy)
        check_process = Process(target=Schedule.check_pool)
        valid_process.start()
        check_process.start()