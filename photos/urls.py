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
    path('photo/<int:pk>/generate_description/', views.AI_generate_description, name='AI_generate_description'),  # 新增的路径
    path('category/<int:pk>/delete/', views.delete_category_view, name='delete_category'),
    path('find_similar/', views.find_similar_photos, name='find_similar_photos'),  # 新增的路径
    path('favicon.ico', serve, {'path': 'images/favicon.ico'}),
    path('save_similar_photo/<int:photo_id>/', views.save_similar_photo, name='save_similar_photo'),
    path('add_site_comment/', views.add_site_comment, name='add_site_comment'),
]
