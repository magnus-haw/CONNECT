"""dppConnect URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path,include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('', include('main.urls')),
    path("feedback/", include('feedback.urls')),
    path("surveys/", include("survey.urls")),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [path("__debug__/", include(debug_toolbar.urls)),] + urlpatterns

if settings.STATIC_URL == "/static/":
    from django.conf.urls.static import static
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)