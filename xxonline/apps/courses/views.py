from django.shortcuts import render
from django.views.generic import View

from courses.models import Course

from pure_pagination import Paginator, PageNotAnInteger

# Create your views here.

class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by("-add_time")
        #
        hot_courses = Course.objects.all().order_by("-click_nums")[:3]
        #
        # #课程搜索
        # search_keywords = request.GET.get('keywords', "")
        # if search_keywords:
        #     all_courses = all_courses.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords)|Q(detail__icontains=search_keywords))
        #
        #课程排序
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")
        #
        #对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 5, request=request)

        courses = p.page(page)

        return render(request, 'course-list.html', {
            "all_courses":courses,
            "sort":sort,
            "hot_courses":hot_courses
        })


class CourseDetailView(View):
    """
    课程详情页
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        # #增加课程点击数
        # course.click_nums += 1
        # course.save()
        #
        # #是否收藏课程
        # has_fav_course = False
        # #是否收藏机构
        # has_fav_org = False
        #
        # if request.user.is_authenticated():
        #     if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
        #         has_fav_course = True
        #
        #     if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
        #         has_fav_org = True
        #
        # tag = course.tag
        # if tag:
        #     relate_coures = Course.objects.filter(tag=tag)[:1]
        # else:
        #     relate_coures = []
        return render(request, "course-detail.html", {
            "course":course,
            # "relate_coures":relate_coures,
            # "has_fav_course":has_fav_course,
            # "has_fav_org":has_fav_org
        })
