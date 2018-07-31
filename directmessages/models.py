from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from django.utils.encoding import python_2_unicode_compatible
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


@python_2_unicode_compatible
class Message(models.Model):
    """
    A private directmessage
    """
    content = models.TextField(_('Content'))
    sender = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='sent_dm', verbose_name=_("Sender"))
    recipient = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='received_dm', verbose_name=_("Recipient"))
    sent_at = models.DateTimeField(_("sent at"), auto_now_add=True)
    read_at = models.DateTimeField(_("read at"), null=True, blank=True)

    class Meta:
        ordering = ['-sent_at']

    @property
    def unread(self):
        """returns whether the message was read or not"""
        if self.read_at is not None:
            return False
        return True

    def __str__(self):
        return self.content

    def save(self, **kwargs):
        if self.sender == self.recipient:
            raise ValidationError("You can't send messages to yourself")

        if not self.id:
            self.sent_at = timezone.now()
        super(Message, self).save(**kwargs)


class ChatRoom(models.Model):
    """
    A private chat room.
    """
    sender = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='chatroom_sender', verbose_name=_("Sender"))
    recipient = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='chatroom_receiver', verbose_name=_("Recipient"))
    created_at = models.DateTimeField(_("sent at"), auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('sender', 'recipient',)