from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('save_points',views.save_points,name='save_points'),
    path('get_save_point',views.get_save_point, name='get_save_point'),
    path('post_save_points/', views.post_save_points, name='post_save_points'),
    
    path('danger_area/', views.danger_area, name='danger_area'),
    path('get_danger_area/', views.get_danger_area, name='get_danger_area'),
    path('post_danger_area/', views.post_danger_area, name='post_danger_area'),
    
]