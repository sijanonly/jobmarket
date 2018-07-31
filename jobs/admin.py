from django.contrib import admin

# Register your models here.

from .models import Job, JobProposal


class JobModelAdmin(admin.ModelAdmin):
    """
    Admin table for SolarCalculator model.

    """
    class Meta:
        model = Job


class ProposalModelAdmin(admin.ModelAdmin):
    """
    Admin table for SolarCalculator model.

    """
    class Meta:
        model = JobProposal


admin.site.register(Job, JobModelAdmin)
admin.site.register(JobProposal, ProposalModelAdmin)
