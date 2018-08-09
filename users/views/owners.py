from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

# from ..decorators import owner_required
from ..forms import CompanySignUpForm
from ..models import User



class SignUpView(CreateView):
    model = User
    form_class = CompanySignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        """Updates current context with 'user_type' to indicate current user type.
        """
        kwargs['user_type'] = 'project owner'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        """Checks form valid and login the current signup user and redirect to job list.
        """
        user = form.save()
        login(self.request, user)
        return redirect('jobs:job_list')


