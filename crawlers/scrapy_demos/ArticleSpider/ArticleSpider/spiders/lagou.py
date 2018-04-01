# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from utils.common import get_cookie, get_md5
from items import LagouJobItem, LagouJobItemLoader
from datetime import datetime


class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/']

    rules = (
        Rule(LinkExtractor(allow=('zhaopin/.*')), follow=True),
        Rule(LinkExtractor(allow=('gongsi/j\d+.html')), follow=True),
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_job', follow=True),
    )

    cookie_str ='''
        WEBTJ-ID=20180331210228-1627c26f0e012a-038155db280944-36465e60-1044480-1627c26f0e1da; 
        user_trace_token=20180331210232-c64094bb-34e3-11e8-a971-525400f775ce;
        LGUID=20180331210232-c6409866-34e3-11e8-a971-525400f775ce; 
        index_location_city=%E4%B8%8A%E6%B5%B7; 
        JSESSIONID=ABAAABAAAGFABEFC938F640C9B25840FA8D0451CD1166A6; 
        TG-TRACK-CODE=index_navigation; SEARCH_ID=744023640745421e9ecf4551755f932f; 
        X_HTTP_TOKEN=31bc74b8989b9c7dce2c46fd7b8ecef7; 
        _gat=1; PRE_UTM=m_cf_cpc_baidu_pc; PRE_HOST=www.baidu.com; 
        PRE_SITE=https%3A%2F%2Fwww.baidu.com%2Fbaidu.php%3Fsc.af0000jT6JN_mhQrXjNZVCAhcz3fFR6LdHAvSlwlNCOrX7T41EAhlQCrAR-LFukxfBdcwgRTP0kTzOesmPZKg0F9U_NFCdJxmm_Hi1bbxFksg0m2a-DY0h_re_nkeKr7cC-OymqR0JsUciJPw6y5yCTZj3NcyprGGNqhgR99N1kCEeuHCf.7D_NR2Ar5Od663rj6tJQrGvKD7ZZKNfYYmcgpIQC8xxKfYt_U_DY2yP5Qjo4mTT5QX1BsT8rZoG4XL6mEukmryZZjzL4XNPIIhExz4rMThEgz3x5Gse5gj_L3x5x9L4n5VLJN9h9moLIrzVf.U1Yk0ZDqs2v4_sK9uZ745TaV8Un0mywkIjYz0ZKGm1Yk0Zfqs2v4_sKGUHYznWR0u1dsThc0Iybqmh7GuZR0TA-b5Hb0mv-b5HDYn6KVIjYknjDLg1DsnH-xnH0zndt1njDdg1nvnjD0pvbqn0KzIjYkPjf0uy-b5HDYPHuxnWDsrHKxnW04nWT0mhbqnW0Y0AdW5HT1njDYP1m4P7tLn10kPjTLnjPxnNtknjFxn0KkTA-b5H00TyPGujYs0ZFMIA7M5H00mycqn7ts0ANzu1Ys0ZKs5H00UMus5H08nj0snj0snj00Ugws5H00uAwETjYs0ZFJ5H00uANv5gKW0AuY5H00TA6qn0KET1Ys0AFL5HDs0A4Y5H00TLCq0ZwdT1Y3nHn4njbvPHfLPjT3PjTvPW0d0ZF-TgfqnHRznWRsPHmsnjb4nsK1pyfqrjTsmHfsn16snj0suHFBu6KWTvYqPWmYwRcznDwjfRc3nWn3wfK9m1Yk0ZK85H00TydY5H00Tyd15H00XMfqn0KVmdqhThqV5HKxn7tsg1Kxn0Kbmy4dmhNxTAk9Uh-bT1Ysg1Kxn7t1nHb4nWKxn0Ksmgwxuhk9u1Ys0AwWpyfqn0K-IA-b5iYk0A71TAPW5H00IgKGUhPW5H00Tydh5HDv0AuWIgfqn0KhXh6qn0Khmgfqn0KlTAkdT1Ys0A7buhk9u1Yk0Akhm1Ys0APzm1YdP1c4%26ck%3D5894.2.103.322.145.274.139.873%26shh%3Dwww.baidu.com%26sht%3Dbaidu%26ie%3Dutf-8%26f%3D8%26tn%3Dbaidu%26wd%3D%25E6%258B%2589%25E9%2592%25A9%26oq%3Dcmder%26rqlang%3Dcn%26inputT%3D1933%26bc%3D110101%26us%3D1.1431174.2.0.1.300.0.0; 
        PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Flp%2Fhtml%2Fcommon.html%3Futm_source%3Dm_cf_cpc_baidu_pc%26m_kw%3Dbaidu_cpc_bj_e110f9_265e1f_%25E6%258B%2589%25E9%2592%25A9; 
        _ga=GA1.2.19867862.1522501350; 
        _gid=GA1.2.19182890.1522501350; 
        LGSID=20180331225649-bd9d648e-34f3-11e8-b6a7-5254005c3644;
        LGRID=20180331225728-d4f27471-34f3-11e8-a9c7-525400f775ce; 
        Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1522505602,1522507035,1522508208,1522508247; 
        Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1522508247
    '''

    # 对请求的返回进行处理的配置
    meta = {
        'dont_redirect': True,  # 禁止网页重定向
        'handle_httpstatus_list': [301, 302],  # 对哪些异常返回进行处理
        # 'cookiejar':1,

    }

    def start_requests(self):
        cookies = get_cookie(self.cookie_str)
        yield scrapy.Request(url=self.start_urls[0], cookies=cookies, meta=self.meta)


    def parse_job(self, response):
        item_loader = LagouJobItemLoader(item=LagouJobItem(), response=response)
        item_loader.add_css('title','.job-name::attr(title)')
        item_loader.add_value('url', response.url)
        item_loader.add_value('url_object_id', get_md5(response.url))
        item_loader.add_css('salary', '.job_request .salary::text')
        item_loader.add_xpath('job_city', '//*[@class="job_request"]/p/span[2]/text()')
        item_loader.add_xpath('work_years', '//*[@class="job_request"]/p/span[3]/text()')
        item_loader.add_xpath('degree_need', '//*[@class="job_request"]/p/span[4]/text()')
        item_loader.add_xpath('job_type', '//*[@class="job_request"]/p/span[5]/text()')
        item_loader.add_css('tags', '.position-label li::text')
        item_loader.add_css('publish_time', '.publish_time::text')
        item_loader.add_css('job_advantage', '.job-advantage p::text')
        item_loader.add_css('job_desc', '.job_bt div') #只提取html，不提取text
        item_loader.add_css('job_addr', '.work_addr') #同上
        item_loader.add_css('company_name', '#job_company dt a img::attr(alt)')
        item_loader.add_css('company_url', '#job_company dt a::attr(href)')
        item_loader.add_value('crawl_time', datetime.now())
        job_item = item_loader.load_item()
        return job_item




