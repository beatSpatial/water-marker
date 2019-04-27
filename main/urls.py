from django.conf.urls import url
from django.contrib import admin
from main import views

urlpatterns = [
  url(r'^admin/', admin.site.urls),
  url(r'^$', views.home, name='index'),
  url(r'^upload_student_list', views.upload_student_list, name='upload-student-list'),
  url(r'^upload_scaffold', views.upload_scaffold, name='upload-scaffold'),
  url(r'^get_cohort_options', views.get_cohort_options, name='get-cohort-options'),
  url(r'^get_class_options', views.get_class_options, name='get-class-options'),
  url(r'^get_students', views.get_students, name='get-students'),
  url(r'^make_watermark', views.make_watermark, name='make-watermarks'),
]

