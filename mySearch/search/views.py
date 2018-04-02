from django.shortcuts import render

# Create your views here.

from django.views.generic.base import View
from search.models import ArticleType
from django.http import HttpResponse
from elasticsearch import Elasticsearch
from elasticsearch_dsl.search import Search
import json
from datetime import datetime
import redis

redis_cli = redis.StrictRedis()
client = Elasticsearch(hosts=["127.0.0.1:9200"])

class SearchSuggest(View):
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

class SearchView(View):
    def get(self, request):
        key_words = request.GET.get("q", "")
        page = request.GET.get("p", "1")
        try:
            page = int(page)
        except:
            page = 1
        jobbole_count = redis_cli.get("jobbole_count").decode()
        start_time = datetime.now()
        response = client.search(
            index="jobbole",
            body={
                "query": {
                    "multi_match": {
                        "query": key_words,
                        "fields": ["tags", "title", "content"]
                    }
                },
                "from": (page)*10,
                "size": 10,
                "highlight": {
                    "pre_tags": ['<span class="keyWord">'],
                    "post_tags": ['</span>'],
                    "fields": {
                        "title": {},
                        "content": {},
                    }
                }
            }
        )

        end_time = datetime.now()
        last_seconds = (end_time - start_time).total_seconds()
        total_nums = response["hits"]["total"]
        if (page % 10) > 0:
            page_nums = int(total_nums / 10) + 1
        else:
            page_nums = int(total_nums / 10)
        hit_list = []
        for hit in response["hits"]["hits"]:
            hit_dict = {}
            if "highlight" in hit and "title" in hit["highlight"]:
                hit_dict["title"] = "".join(hit["highlight"]["title"])
            else:
                hit_dict["title"] = hit["_source"]["title"]
            if "highlight" in hit and "content" in hit["highlight"]:
                hit_dict["content"] = "".join(hit["highlight"]["content"])[:500]
            else:
                hit_dict["content"] = hit["_source"]["content"][:500]

            hit_dict["create_date"] = hit["_source"]["create_date"]
            hit_dict["url"] = hit["_source"]["url"]
            hit_dict["score"] = hit["_score"]

            hit_list.append(hit_dict)
        return render(request, "result.html", {"page":page,
                                                   "all_hits": hit_list,
                                                   "key_words": key_words,
                                                   "total_nums": total_nums,
                                                    "last_seconds": last_seconds,
                                                    "jobbole_count": jobbole_count,
                                                    "page_nums":page_nums
                                                   })
