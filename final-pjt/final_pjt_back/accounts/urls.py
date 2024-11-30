from django.urls import path
# from .views import UpdateProfileView
from . import views
urlpatterns = [
    # path('signup/', views.signup)
    path('profile/', views.profile),
    path('signout/', views.signout),
    path('user_info/', views.user_info),
    #  path('accounts/updateprofile/', views.CustomProfileUpdateView.as_view()),
    # path('accounts/updateprofile/', views.update_profile, name='update_profile'),
    # path('updateprofile/', UpdateProfileView.as_view()),
]