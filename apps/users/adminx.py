__author__ = 'yuchen'
__date__ = '2018/4/31 22:59'
import xadmin
from .models import EmailVerifyRecord,Banner
from xadmin import views#引入xadmin的主题页面视图函数

#主题定制修改
class BaseSetting(object):
    enable_themes=True
    use_bootswatch=True

class GlogbalSettings(object):
    site_title='abc360后台管理系统'
    site_footer='abc360官网'
    menu_style='accordion'


class EmailVerifyRecordAdmin(object):
    list_display=['code','email','send_type','send_time']
    search_fields=['code','email','send_type',]
    list_filter=['code','email','send_type','send_time']

class BannerAdmin(object):
    list_display=['title','image','url','index','add_time']
    search_field=['title','image','url','index','add_time']
    list_filter=['title','image','url','index']

xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)#注册主题
xadmin.site.register(views.CommAdminView,GlogbalSettings)


