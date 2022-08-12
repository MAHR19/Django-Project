from django.urls import path

from . import views

app_name = 'pollsv2'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/',  views.detail, name='detail'),
    path('<int:pk>/',  views.results, name='results'),
    path('<int:question_id>/',  views.vote, name='vote'),
]

