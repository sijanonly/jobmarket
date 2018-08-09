from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView, UpdateView
from django.views.generic.detail import DetailView

# Create your views here.
from ..models import User
from ..forms import SignUpForm


def home(request):
    """Renders home template.
    """
    return render(request, 'allwork/home.html')


class SignUpView(TemplateView):
    """
    Renders signup select page (freelancer / project owner)
    """
    template_name = 'registration/signup.html'


# class UserRegister(CreateView):
#     model = User
#     form_class = SignUpForm
#     template_name = 'signup.html'


class UserJobProfile(TemplateView):

    model = User
    template_name = 'allwork/jobs/job_profile.html'

    def get_context_data(self, **kwargs):
        """Prepares user context value based on username request from url.
        """
        context = super(UserJobProfile, self).get_context_data(**kwargs)
        username = self.kwargs.get('username')
        context['profile'] = User.objects.get(username=username)
        return context


class UserDetailView(TemplateView):

    model = User
    template_name = 'allwork/freelancers/user_profile.html'

    def get_context_data(self, **kwargs):
        """Prepares user context value based on username request from url.
        """
        context = super(UserDetailView, self).get_context_data(**kwargs)
        username = self.kwargs.get('username')
        context['profile'] = User.objects.get(username=username)
        return context


class UpdateProfileView(UpdateView):
    model = User
    fields = ['avatar', 'first_name', 'last_name', 'profile', 'skills']  # Keep listing whatever fields
    template_name = 'allwork/freelancers/user_profile_update.html'

    def form_valid(self, form):
        """Checks valid form and add/save many to many tags field in user object.
        """
        user = form.save(commit=False)

        user.save()
        form.save_m2m()
        messages.success(self.request, 'Your profile is updated successfully!')
        return redirect('users:user_profile', self.object.username)

    def get_success_url(self):
        """
        Prepares success url for successful form submission.
        """
        return reverse('users:user_profile', kwargs={'username': self.object.username})
