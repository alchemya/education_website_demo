from django.shortcuts import render

# Create your views here.
from django.views.generic import View
from organization.models import CourseOrg,CityDict
from pure_pagination import Paginator,EmptyPage,PageNotAnInteger
from .forms import UserAskForm
from django.http import HttpResponse,JsonResponse
from courses.models import Course
from operation.models import UserFavorite
from .models import Teacher

class OrgView(View):
    """
    课程机构列表
    """
    def get(self,request):
        # 取出所有课程机构
        all_orgs = CourseOrg.objects.all()

        # 取出所有城市
        all_citys = CityDict.objects.all()

        city_id=request.GET.get('city','')
        if city_id:
            all_orgs=all_orgs.filter(city_id=int(city_id))

        # 类别筛选
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        sort = request.GET.get('sort', "null")
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")

        # 有多少家机构
        org_nums = all_orgs.count()

        # 对课程机构进行分页
        # 尝试获取前台get请求传递过来的page参数
        # 如果是不合法的配置参数默认返回第一页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 这里指从allorg中取2个出来，每页显示2个
        p = Paginator(all_orgs, 2, request=request)
        orgs = p.page(page)
        org_nums = all_orgs.count()

        hot_orgs = all_orgs.order_by('-click_nums')[:3]



        return render(request, "org-list.html", {
            "all_orgs": orgs,
            "all_citys": all_citys,
            "org_nums": org_nums,
            'city_id': city_id,
            'category':category,
            'hot_orgs':hot_orgs,
            'sort':sort
        })

class AddUserAskView(View):
    """
    用户添加咨询
    """
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            userask_form.save(commit=True)
            # 如果保存成功,返回json字符串,后面content type是告诉浏览器返回的数据类型
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            # 如果保存失败，返回json字符串,并将form的报错信息通过msg传递到前端
            return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json')

def try_fav(request,course_org):
    if request.user.is_authenticated():
        if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
            has_fav = True
            return has_fav
        else:
            has_fav =False
            return has_fav

class OrgHomeView(View):
    '''机构首页'''

    def get(self,request,org_id):
        # 根据id找到课程机构
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav=try_fav(request,course_org)
        # 反向查询到课程机构的所有课程和老师
        all_courses = course_org.course_set.all()[:4]
        all_teacher = course_org.teacher_set.all()[:2]
        return render(request,'org-detail-homepage.html',{
            'course_org':course_org,
            'all_courses':all_courses,
            'all_teacher':all_teacher,
            'current_page': current_page,
            'has_fav':has_fav
        })

class OrgCourseView(View):
    """
   机构课程列表页
    """
    def get(self, request, org_id):
        current_page='course'

        # 根据id取到课程机构
        course_org = CourseOrg.objects.get(id= int(org_id))
        # 通过课程机构找到课程。内建的变量，找到指向这个字段的外键引用
        all_courses = course_org.course_set.all()
        has_fav = try_fav(request, course_org)

        return render(request, 'org-detail-course.html',{
           'all_courses':all_courses,
            'course_org': course_org,
            'current_page':current_page,
            'has_fav': has_fav
        })

class OrgDescView(View):
    '''机构介绍页'''
    def get(self, request, org_id):
        current_page = 'desc'
        # 根据id取到课程机构
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav=try_fav(request,course_org)



        return render(request, 'org-detail-desc.html',{
            'course_org': course_org,
            'current_page':current_page,
            'has_fav': has_fav
        })

class OrgTeacherView(View):
    """
   机构教师页
    """
    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id= int(org_id))
        all_teacher = course_org.teacher_set.all()

        has_fav=try_fav(request,course_org)

        return render(request, 'org-detail-teachers.html',{
           'all_teacher':all_teacher,
            'course_org': course_org,
            'current_page':current_page,
            'has_fav':has_fav
        })

class AddUserFav(View):
    """
        用户收藏和取消收藏
        """

    def post(self, request):
        id = request.POST.get('fav_id', 0)  # 防止后边int(fav_id)时出错
        type = request.POST.get('fav_type', 0)  # 防止int(fav_type)出错

        if not request.user.is_authenticated:
            # 未登录时返回json提示未登录，跳转到登录页面是在ajax中做的
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        exist_record = UserFavorite.objects.filter(user=request.user, fav_id=int(id), fav_type=int(type))
        if exist_record:
            # 如果记录已经存在，表示用户取消收藏
            exist_record.delete()
            # return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
            return JsonResponse({"status":"success", "msg":"收藏"})
        else:
            user_fav = UserFavorite()
            if int(id) > 0 and int(type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(id)
                user_fav.fav_type = int(type)
                user_fav.save()
                # return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
                return JsonResponse({"status":"success", "msg":"已收藏"})
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')

class TeacherListView(View):
    def get(self, request):
        all_teachers = Teacher.objects.all()
        # 总共有多少老师使用count进行统计
        teacher_nums = all_teachers.count()

        # 人气排序
        sort = request.GET.get('sort','')
        if sort:
            if sort == 'hot':
                all_teachers = all_teachers.order_by('-click_nums')

        #讲师排行榜
        sorted_teacher = Teacher.objects.all().order_by('-click_nums')[:3]
        # 进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, 1, request=request)
        teachers = p.page(page)
        return render(request, "teachers-list.html", {
            "all_teachers": teachers,
            "teacher_nums": teacher_nums,
            'sorted_teacher':sorted_teacher,
            'sort':sort,
        })


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        all_course = Course.objects.filter(teacher=teacher)

        # 教师收藏和机构收藏
        has_teacher_faved = False
        if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
            has_teacher_faved = True

        has_org_faved = False
        if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
            has_org_faved = True

        # 讲师排行榜
        sorted_teacher = Teacher.objects.all().order_by('-click_nums')[:3]
        return render(request, 'teacher-detail.html', {
            'teacher': teacher,
            'all_course': all_course,
            'sorted_teacher': sorted_teacher,
            'has_org_faved':has_org_faved,
            'has_teacher_faved':has_teacher_faved
        })