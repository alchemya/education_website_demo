__author__ = 'yuchen'
__date__ = '2018/7/31 23:19'

from  .models import Course,Lesson,Video,CourseResourse
import xadmin

class CourseAdmin(object):
    list_display=['name','course_org','desc','degree','learn_times','students','fav_nums','image','click_nums','add_time']
    search_fields=['name','desc','degree','learn_times','students','fav_nums','image','click_nums','add_time']
    list_filter=['name','desc','degree','learn_times','students','fav_nums','image','click_nums']

class LessonAdmin(object):
    list_display=['course','name','add_time']
    search_fields=['course','name','add_time']
    list_filter=['course__name','name','add_time']

class ViedoAdmin(object):
    list_display=['lesson','name','add_time']
    search_fields=['lesson','name','add_time']
    list_filter=['lesson__name','name','add_time']

class CourseResourseAdmin(object):
    list_display=['course','name','add_time','download']
    search_fields=['course','name','add_time','download']
    list_filter=['course__name','name','add_time']


xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Video,ViedoAdmin)
xadmin.site.register(CourseResourse,CourseResourseAdmin)