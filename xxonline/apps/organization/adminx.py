from .models import CityDict, CourseOrg
import xadmin

class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']
    model_icon = 'fa fa-university'


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_nums', 'fav_nums']
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums']
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums']
    relfield_style = 'fk-ajax'
    # style_fields = {"desc":"ueditor"}
    model_icon = 'fa fa-university'


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)