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
from django.views.generic import TemplateView

from django.db.models import Q
from django.views.generic.base import RedirectView

from jobs.models import Job, JobProposal
from users.models import User

from .models import Message, ChatRoom
from .services import MessagingService
from .forms import MessageForm
# Create your views here.


class MessageDetailView(CreateView):
    model = ChatRoom
    form_class = MessageForm
    template_name = 'allwork/messages/message.html'

    def get_context_data(self, **kwargs):
        chat_id = self.kwargs.get('pk')

        chatroom = ChatRoom.objects.get(pk=chat_id)

        print('chatroom is', chatroom)

        message = Message.objects.filter(
            sender=chatroom.sender,
            recipient=chatroom.recipient).first()
        if not message:
            message = Message.objects.filter(
                sender=chatroom.recipient,
                recipient=chatroom.sender).first()

        # MessagingService().mark_as_read(message)
        print('i am called......')
        user = self.request.user

        print('message is', message)

        kwargs['active_conversation'] = message
        current_conversations = MessagingService().get_conversations(user=self.request.user)
        # current_conversations = MessagingService().get_conversations(user=message.recipient)
        kwargs['conversations'] = current_conversations
        # kwargs['conversations'] = [conv for conv in current_conversations if message.pk != conv.pk]

        if user == message.sender:
            active_recipient = message.recipient
        else:
            active_recipient = message.sender
        running_conversations = MessagingService().get_active_conversations(user, active_recipient)
        kwargs['running_conversations'] = running_conversations

        # kwargs['form'] = MessageForm
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        obj = self.get_object()

        if self.request.user == obj.sender:
            recipient = obj.recipient
        else:
            recipient = obj.sender

        message = form.save(commit=False)
        message.sender = self.request.user
        message.recipient = recipient

        message.save()
        messages.success(self.request, 'The message is sent with success!')
        return redirect('messages:user_message', obj.pk)

@method_decorator([login_required], name='dispatch')
class MessageView(RedirectView):

    permanent = False
    query_string = True
    pattern_name = 'messages:user_message'

    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user

        chatroom = ChatRoom.objects.filter(Q(sender=user) | Q(recipient=user)).first()
        if chatroom:
            return super().get_redirect_url(*args, pk=chatroom.pk)
        else:
            messages.warning(self.request, 'You do not have any messages to show')
            return reverse('jobs:job_list')
