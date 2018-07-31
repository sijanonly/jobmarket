# -*- coding: utf-8 -*-
# @Author: Sijan
# @Date:   2018-07-27 19:36:49
# @Last Modified time: 2018-07-27 22:31:20

from django.contrib import admin
from django.urls import path, include

from .views import (MessageView, MessageDetailView)


urlpatterns = [
    path('messages/', include(([
        path('', MessageView.as_view(), name='list_message'),
        path('<int:pk>/', MessageDetailView.as_view(), name='user_message'),
    ], 'messages'), namespace='messages')),
]
