__author__ = 'yuchen'
__date__ = '2018/10/5 02:22'

from django.conf.urls import url,include
from .views import OrgView,AddUserAskView,OrgHomeView,OrgCourseView,OrgDescView,OrgTeacherView,AddUserFav,\
    TeacherListView,TeacherDetailView

urlpatterns = [

    url(r'^list/$',OrgView.as_view(),name='org_list'),
    url(r'^add_ask$',AddUserAskView.as_view(),name='add_ask'),
    url(r'^home/(?P<org_id>\d+)/$',OrgHomeView.as_view(),name='org_home'),
    url(r'^course/(?P<org_id>\d+)/$',OrgCourseView.as_view(),name='org_course'),
    url(r'^desc/(?P<org_id>\d+)/$',OrgDescView.as_view(),name='org_desc'),
    url(r'^teacher/(?P<org_id>\d+)/$',OrgTeacherView.as_view(),name='org_teacher'),

    url(r'^add_fav/$',AddUserFav.as_view(),name='add_fav'),

    url('teacher/list/', TeacherListView.as_view(), name="teacher_list"),
    url('teacher/detail/(?P<teacher_id>\d+)/', TeacherDetailView.as_view(), name="teacher_detail"),
]