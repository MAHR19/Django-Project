from django.urls import path

from . import views


app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('register', views.RegistrationView, name='register'),
    path('login',views.login_user, name='login_user'),
    path('logout',views.logoutView, name='logout'),
    path('profile',views.profileview,name='my_profile'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
