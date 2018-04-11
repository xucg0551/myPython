from courses.models import Course
import xadmin

class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    ordering = ['-click_nums']
    readonly_fields = ['click_nums']
    list_editable = ['degree', 'desc']
    exclude = ['fav_nums']
    # inlines = [LessonInline, CourseResourceInline]
    # style_fields = {"detail":"ueditor"}
    # import_excel = True

    # def queryset(self):
    #     qs = super(CourseAdmin, self).queryset()
    #     qs = qs.filter(is_banner=False)
    #     return qs
    #
    # def save_models(self):
    #     #在保存课程的时候统计课程机构的课程数
    #     obj = self.new_obj
    #     obj.save()
    #     if obj.course_org is not None:
    #         course_org = obj.course_org
    #         course_org.course_nums = Course.objects.filter(course_org=course_org).count()
    #         course_org.save()
    #
    # def post(self, request, *args, **kwargs):
    #     if 'excel' in request.FILES:
    #         pass
    #     return super(CourseAdmin, self).post(request, args, kwargs)


xadmin.site.register(Course, CourseAdmin)