from django.conf.urls import url,include
from .views import CourseListView,CourseDetailView,CourseInfoView,CommentsView,AddCommentsView, VideoPlayView
# 要写上app的名字


urlpatterns = [
    url(r'^list/$',CourseListView.as_view(),name='course_list'),
    url('course/(?P<course_id>\d+)/', CourseDetailView.as_view(), name="course_detail"),
    url('info/(?P<course_id>\d+)/', CourseInfoView.as_view(), name="course_info"),
    url('comment/(?P<course_id>\d+)/', CommentsView.as_view(), name="course_comments"),
    url('add_comment/', AddCommentsView.as_view(), name="add_comment"),
    url('video/(?P<video_id>\d+)/', VideoPlayView.as_view(), name="video_play"),
]