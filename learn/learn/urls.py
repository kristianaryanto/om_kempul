
from django.contrib import admin
from django.urls import path,include, re_path
from django.conf.urls.static import static,serve

from . import settings
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # re_path(r'^(?P<tahun>[0-9]{4})/(?P<bulan>[0-9]{2})/(?P<tanggal>[0-9]{2})/$', views.about),
    path('blog/',include('blog.urls')),
    path('',include('csvs.urls', namespace='csvs')),
    path('user_manage/',include('user_manage.urls',namespace='user_manage')),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root':  settings.MEDIA_ROOT}), 
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATICFILES_DIRS}), 
]

# urlpatterns = static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
