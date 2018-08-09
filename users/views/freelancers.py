# -*- coding: utf-8 -*-
# @Author: leapfrong
# @Date:   2018-07-22 18:01:25
# @Last Modified by:   leapfrong
# @Last Modified time: 2018-08-06 16:09:22

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView

from ..forms import FreelancerSignUpForm
from ..models import User


class SignUpView(CreateView):
    model = User
    form_class = FreelancerSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        """Updates context value 'user_type' in curernt context.
        """
        kwargs['user_type'] = 'freelancer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        """Checks for valid form and call login for current signup user and
        redirect to job list page.
        """
        user = form.save()
        login(self.request, user)
        return redirect('jobs:job_list')


class ListFreelancerView(ListView):
    model = User
    context_object_name = 'freelancers'
    template_name = 'allwork/freelancers/freelancer_list.html'

    def get_queryset(self):
        """Prepare all freelancers based on is_freelancer col in user model.
        """
        return User.objects.filter(is_freelancer=True)
