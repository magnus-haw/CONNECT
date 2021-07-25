from django.contrib import admin
from django.urls import path

from .views import contactView, successView, emailListView

urlpatterns = [
    path('contact/', contactView, name='contact'),
    path('success/', successView, name='success'),
    path('list/<int:list_pk>', emailListView, name='list-detail'),
]
