import xadmin
from .models import Banner, UserProfile, EmailVerifyRecord
from xadmin import views


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "cg后台管理系统"
    site_footer = "cg在线网"
    # menu_style = 'default'  # 'accordion'


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']
    model_icon = 'fa fa-arrows'


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']
    model_icon = 'fa fa-share'


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.unregister(UserProfile)
xadmin.site.register(UserProfile)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)


