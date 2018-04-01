from django.shortcuts import render

# Create your views here.

from django.views.generic.base import View
from search.models import ArticleType
from django.http import HttpResponse
from elasticsearch import Elasticsearch
from elasticsearch_dsl.search import Search
import json

client = Elasticsearch(hosts=["127.0.0.1:9200"], timeout=5000)

class SearchSuggest(View):
    # def set_suggest_optional(self, key_words, suggest_size):
    #     # 检索选项
    #     es_suggest_options = {
    #         "suggest": {
    #             "my-suggestion": {
    #                 "text": key_words,
    #                 "completion": {
    #                     "field": "suggest",
    #                     "fuzzy": {
    #                         "fuzziness": 2
    #                     },
    #                     "size": suggest_size
    #                 }
    #             }
    #         },
    #         "_source": "title"
    #     }
    #     return es_suggest_options
    #
    # def suggest(self, query, suggest_size=10):
    #     # 设置条件
    #     es_suggest_options = self.set_suggest_optional(query, suggest_size)
    #     # 发起检索。
    #
    #     es_result = client.suggest(index='index', body=es_suggest_options)
    #     print(es_result)
    #         # 得到结果。
    #     # final_results = get_suggest_list(es_result)
    #     # return final_results
    #
    # def get(self, request):
    #     key_words = request.GET.get('s', '')
    #
    #     if key_words:
    #         self.suggest(key_words)
    #
    #     return HttpResponse(json.dumps("12345"), content_type="application/json")


    def get(self, request):
        key_words = request.GET.get('s', '')
        re_datas = []
        if key_words:
            s = ArticleType.search().suggest('my_suggestions', key_words, completion={
                "field": "suggest",
                'size':10
            })

            response = s.execute()
            for match in response.suggest.my_suggestions[0].options:
                 source = match._source
                 re_datas.append(source["title"])
        return HttpResponse(json.dumps(re_datas))
