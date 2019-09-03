from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('new-post', views.NewPost.as_view(), name='new_post'),
    path('', views.Index.as_view(), name='index'),
]
