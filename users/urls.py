from django.urls import include, path

from .views import common, freelancers, owners

urlpatterns = [
    path('', common.home, name='home'),
    # path('user/<slug:username>/jobs', common.UserJobProfile.as_view(), name='job_profile',
    #      namespace='users'),

    # path('user/<slug:username>/', include([
    #     path('jobs/', common.UserJobProfile.as_view(), name='job_profile'),
    # ]), namespace='users'),

    path('user/<str:pk>/edit', common.UpdateProfileView.as_view(), name='update_profile'),
    path('user/<str:username>/', include(([
        path('', common.UserDetailView.as_view(), name='user_profile'),
        path('jobs/', common.UserJobProfile.as_view(), name='job_profile'),
    ], 'users'), namespace='users')),
]
