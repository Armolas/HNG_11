from django.urls import path
from .views import (
        RegisterView,
        LoginView,
        UserView,
        LogoutView,
        OrgsView,
        OrgView
        )

urlpatterns = [
        path('auth/register', RegisterView.as_view()),
        path('auth/login', LoginView.as_view()),
        path('api/users/<str:userId>', UserView.as_view()),
        path('auth/logout', LogoutView.as_view()),
        path('api/organisations', OrgsView.as_view()),
        path('api/organisations/<str:orgId>', OrgView.as_view()),
        path('api/organisations/<str:orgId>/users', OrgView.as_view()),
        ]
