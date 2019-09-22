"""abc360Online URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
import xadmin
from django.views.generic import TemplateView
# from users.views import log_in
from users.views import LoginView,RegisterView,ActiveView,ForgetPassView,Reset,ChangepwdView
from django.contrib.auth import views as auth_views
from organization.views import OrgView
from django.conf.urls.static import static
from django.conf import settings
from courses.views import CourseListView

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$',TemplateView.as_view(template_name='index.html'),name='index'),
    # url(r'^login/$',log_in,name='login')
    url(r'^login/$',LoginView.as_view(),name='login'),
    url(r'^register/$',RegisterView.as_view(),name='register'),
    url(r'^logout/$',auth_views.logout,name='user_logout',),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$',ActiveView.as_view(),name='user_active'),
    url(r'^iforget/$',ForgetPassView.as_view(),name='i_forget'),
    url(r'^reset/(?P<active_code>.*)/$',Reset.as_view(),name='user_reset'),
    url(r'^changepwd/$',ChangepwdView.as_view(),name='change_pwd'),

    url(r'^org/',include('organization.urls',namespace='org')),
    url(r'^course/',include('courses.urls',namespace='course')),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
