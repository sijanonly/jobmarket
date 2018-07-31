from django.shortcuts import render, redirect

from django.urls import reverse
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView, UpdateView
from django.views.generic.detail import DetailView

# Create your views here.
from ..models import User
from ..forms import SignUpForm


def home(request):
    # if request.user.is_authenticated:
    #     if request.user.is_owner:
    #         return redirect('owners:quiz_change_list')
    #     else:
    #         return redirect('freelancers:quiz_list')
    return render(request, 'allwork/home.html')


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


class UserRegister(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'signup.html'

    # def form_valid(self, form):
    #     form.instance.created_by = self.request.user
    #     return super().form_valid(form)


class UserJobProfile(TemplateView):

    model = User
    template_name = 'allwork/jobs/job_profile.html'

    def get_context_data(self, **kwargs):
        context = super(UserJobProfile, self).get_context_data(**kwargs)
        username = self.kwargs.get('username')
        # here's the difference:
        print('uer is', User.objects.get(username=username))
        context['user'] = User.objects.get(username=username)
        return context


class UserDetailView(TemplateView):

    model = User
    template_name = 'allwork/freelancers/user_profile.html'

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        username = self.kwargs.get('username')
        context['user'] = User.objects.get(username=username)
        return context


class UpdateProfileView(UpdateView):
    model = User
    fields = ['first_name', 'last_name']  # Keep listing whatever fields
    template_name = 'allwork/freelancers/user_profile_update.html'


    def get_success_url(self):
        return reverse('users:user_profile', kwargs={'username': self.object.username})
