"""allwork URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, include

from users.views import (common, freelancers, owners)

urlpatterns = [
    path('', include('users.urls')),
    path('', include('jobs.urls')),
    path('', include('directmessages.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('', common.home, name='home'),
    path('accounts/signup/', common.SignUpView.as_view(), name='signup'),
    path('accounts/signup/freelancer/', freelancers.SignUpView.as_view(), name='freelancer_signup'),
    path('accounts/signup/project-owner/', owners.SignUpView.as_view(), name='owner_signup'),
    # path('signin/', UserRegister.as_view()),
]
