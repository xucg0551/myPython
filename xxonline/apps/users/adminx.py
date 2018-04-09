import xadmin
from .models import Banner, UserProfile
from xadmin import views


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "cg学后台管理系统"
    site_footer = "cg在线网"
    # menu_style = 'default'  # 'accordion'


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(Banner, BannerAdmin)
xadmin.site.unregister(UserProfile)
xadmin.site.register(UserProfile)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)


