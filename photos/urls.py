from django.urls import path
from . import views
from django.contrib.staticfiles.views import serve

urlpatterns = [
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),

    path('', views.gallery, name='gallery'),
    path('photo/<str:pk>/', views.viewPhoto, name='photo'),
    path('add/', views.addPhoto, name='add'),
    path('photo/<int:pk>/edit/', views.edit_photo, name='edit_photo'),
    path('photo/<int:pk>/delete/', views.delete_photo, name='delete_photo'),
    path('category/<int:pk>/delete/', views.delete_category_view, name='delete_category'),
    path('favicon.ico', serve, {'path': 'images/favicon.ico'}),
]
