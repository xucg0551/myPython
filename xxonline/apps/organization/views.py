from django.shortcuts import render, HttpResponse
from django.views.generic import View

from pure_pagination import PageNotAnInteger, Paginator
from .models import CityDict, CourseOrg
from .forms import UserAskForm

# Create your views here.

class OrgView(View):
    def get(self, request):
        all_cities = CityDict.objects.all()
        all_orgs = CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by('-click_nums')[:3]
        org_nums = all_orgs.count()

        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id = int(city_id))

        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category = category)

        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 3, request=request)

        orgs = p.page(page)
        return render(request, 'org-list.html',{
            'all_orgs': orgs,
            'all_cities': all_cities,
            'org_nums': org_nums,
            'city_id': city_id,
            'category': category,
            'hot_orgs': hot_orgs,
            "sort": sort
        })

class AddUserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json')

