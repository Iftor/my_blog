from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainPageView.as_view(), name='main_page'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='main_page'), name='logout'),
    path('registration/', views.UserRegistrationView.as_view(), name='registration'),
    path('profile/', views.PersonalAccountView.as_view(), name='personal_account'),
    path('blog/<str:username>', views.UserBlogView.as_view(), name='user_blog'),
]