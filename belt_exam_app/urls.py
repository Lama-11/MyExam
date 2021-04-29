from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login',views.login),
    path('logout', views.logout),
    path('wishes', views.wishes_page),
    path('wishes/new', views.new_wish_page),
    path('create_wish', views.create_wish),
    path('remove/<int:wish_id>', views.remove),
    path('wishes/edit/<int:wish_id>', views.edit_page),
    path('update/<int:current_wish_id>', views.edit),
    path('grant_wish/<int:wish_id>', views.grant_wish),
    path('wishes/stats', views.stat_page),
    path('like/<int:wish_id>', views.like_unlike),
]