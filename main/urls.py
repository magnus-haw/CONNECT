from django.urls import path
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('about', views.about, name='about'),
  path('awards', views.awards,name='awards'),
  path('meeting', views.meeting,name='meeting'),
  path('students', views.students,name='students'),
  path('postdocs', views.postdocs,name='postdocs'),
  path('earlycareer', views.earlycareer,name='earlycareer'),
  path('person/<int:pk>', views.PersonDetailView.as_view(), name='person-detail'),
  path('meeting/<int:pk>', views.MeetingDetailView, name='meeting-detail'),
]
