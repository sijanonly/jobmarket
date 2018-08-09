import os
from django.conf import settings
from django.http import HttpResponse
from django.http import Http404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, ListView, UpdateView
from django.views.generic.detail import DetailView

from django.views.generic.base import RedirectView

from jobs.models import Job, JobProposal
from users.models import User

from directmessages.services import MessagingService
from directmessages.models import ChatRoom
# Create your views here.


class JobListView(ListView):
    model = Job
    ordering = ('job_title', )
    context_object_name = 'jobs'
    template_name = 'allwork/jobs/job_list.html'
    queryset = Job.objects.all()
    paginate_by = 5  #and that's it !!


@method_decorator([login_required], name='dispatch')
class JobCreateView(CreateView):
    model = Job
    fields = ('job_title', 'job_description', 'price', 'tags', 'document')
    template_name = 'allwork/owners/job_add_form.html'

    def form_valid(self, form):
        job = form.save(commit=False)
        job.owner = self.request.user

        job.save()
        form.save_m2m()
        messages.success(self.request, 'The job was created with success!')
        return redirect('jobs:job_detail', job.pk)


@method_decorator([login_required], name='dispatch')
class JobDetailView(DetailView):

    model = Job
    template_name = 'allwork/jobs/job_detail.html'

    def get_context_data(self, **kwargs):
        job_id = self.kwargs.get('pk')
        job = Job.objects.get(pk=job_id)
        if job.owner != self.request.user and self.request.user in job.freelancers:
            kwargs['current_proposal'] = JobProposal.objects.get(
                job__pk=job_id, freelancer=self.request.user)
        context = super().get_context_data(**kwargs)
        return context


class JobApplyView(CreateView):
    model = JobProposal
    fields = ('proposal',)
    template_name = 'allwork/jobs/job_apply_form.html'

    # def get_success_url(self):
    #     return reverse('users:job_profile', kwargs={'slug': self.request.user.username})

    def get_context_data(self, **kwargs):
        kwargs['job'] = Job.objects.get(pk=self.kwargs.get('pk'))
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        # form.instance.job = Job.objects.get(pk=self.kwargs.get('pk'))
        # form.instance.freelancer = self.request.user
        # form.save()

        proposal = form.save(commit=False)
        proposal.job = Job.objects.get(pk=self.kwargs.get('pk'))
        proposal.freelancer = self.request.user

        proposal.save()
        return redirect('users:job_profile', self.request.user.username)


class ProposalAccceptView(RedirectView):

    permanent = False
    query_string = True
    pattern_name = 'jobs:job_detail'

    def get_redirect_url(self, *args, **kwargs):
        job = get_object_or_404(Job, pk=kwargs['pk'])
        job.freelancer = User.objects.get(username=kwargs.get('username'))
        job.status = 'working'
        job.save()

        # Create Message opening
        is_chatroom = False
        try:
            chatroom = ChatRoom.objects.get(sender=self.request.user, recipient=job.freelancer)
            is_chatroom = True
        except:
            pass

        if not is_chatroom:
            try:
                chatroom = ChatRoom.objects.get(sender=job.freelancer, recipient=self.request.user)
            except:
                pass

        if not is_chatroom:
            chatroom = ChatRoom.objects.create(sender=self.request.user, recipient=job.freelancer)

        print('is chatroom', is_chatroom)
        print('chat roo', chatroom)

        print('chat room created....')

        MessagingService().send_message(
            sender=self.request.user,
            recipient=job.freelancer,
            message="""

            Hi {username},

            Your proposal is accepted.

            project details : <a href='{url}'> {job}</a>


            """.format(username=job.freelancer.username,
                       url=reverse("jobs:job_detail", kwargs={"pk": job.pk}),
                       job=job.job_title)

        )

        messages.success(
            self.request, 'User : {} is assiged to your project'.format(kwargs.get('username')))
        return super().get_redirect_url(*args, pk=kwargs['pk'])


class JobCloseView(RedirectView):

    permanent = False
    query_string = True
    pattern_name = 'jobs:job_detail'

    def get_redirect_url(self, *args, **kwargs):
        job = get_object_or_404(Job, pk=kwargs['pk'])
        job.status = 'ended'
        job.save()
        messages.warning(
            self.request, 'Job is ended successfully')
        return super().get_redirect_url(*args, pk=kwargs['pk'])
