# -*- coding: utf-8 -*-
# @Author: Sijan
# @Date:   2018-07-27 22:28:26
# @Last Modified time: 2018-07-27 22:42:37

from django.forms import ModelForm
from django import forms

from .models import Message


class MessageForm(ModelForm):

    content = forms.CharField(
        max_length=1000,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'write_msg', 'name': 'content', 'placeholder': 'Reply...'}
        )
    )

    class Meta:
        model = Message
        fields = ['content']
