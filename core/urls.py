# core/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('year/<int:year_num>/semester/<int:sem_num>/<str:exam_name>/', views.resource_list, name='resource_list'),
    path('year/<int:year_num>/semester/<int:sem_num>/', views.semester_detail, name='semester_detail'),
    path('year/<int:year_num>/', views.year_detail, name='year_detail'),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),  # ← Updated!
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('upgrade/', views.upgrade, name='upgrade'),
]