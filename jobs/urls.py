from django.urls import include, path

from .views import (
    JobListView, JobCreateView, JobDetailView, JobApplyView,
    ProposalAccceptView, JobCloseView)
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('jobs/', include(([
        path('', JobListView.as_view(), name='job_list'),
        path('<int:pk>/', JobDetailView.as_view(), name='job_detail'),
        path('<int:pk>/apply', JobApplyView.as_view(), name='job_apply'),
        path('<int:pk>/close', JobCloseView.as_view(), name='job_close'),
        path('<int:pk>/accept/<str:username>',
             ProposalAccceptView.as_view(), name='proposal_accept'),
        path('add/', JobCreateView.as_view(), name='job_add'),
    ], 'allwork'), namespace='jobs')),

]

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
