from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.utils.html import escape, mark_safe
from taggit.managers import TaggableManager


import uuid

# Create your models here.


class Job(models.Model):
    """
    Model to create a Job.

    """
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name="job_owner",
    )
    freelancer = models.ForeignKey(
        'users.User',
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name="job_freelancer",
    )
    job_title = models.CharField(max_length=300)
    job_description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    tags = TaggableManager()

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    document = models.FileField(upload_to='attachments', blank=True, null=True)

    ACTIVE = 'active'
    WORKING = 'working'
    ENDED = 'ended'
    CHOICES = ((ACTIVE, 'active',), (WORKING, 'working',), (ENDED, 'ended'),)

    status = models.CharField(max_length=9, choices=CHOICES, default=ACTIVE)

    class Meta:
        verbose_name = _('job')
        verbose_name_plural = _('jobs')
        unique_together = ('owner', 'date_created',)

    def __str__(self):
        return "%s - %s - %s" % (
            self.owner.get_full_name(),
            self.freelancer.get_full_name() if self.freelancer else '',
            self.status)

    @property
    def freelancers(self):
        proposals = self.job_proposal.all()
        return [proposal.freelancer for proposal in proposals]


class JobProposal(models.Model):
    """
    Model to create a freelancers's proposal for a JOB.

    """
    job = models.ForeignKey(
        'Job',
        on_delete=models.CASCADE,
        related_name="job_proposal",
    )
    freelancer = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name="job_proposal",
    )
    proposal = models.TextField()

    class Meta:
        unique_together = ('job', 'freelancer')
