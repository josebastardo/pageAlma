from django.urls import path
from . import views

urlpatterns = [
    path('blog/', views.topic_list, name='topic_list'),
    path('topic/<int:pk>/', views.topic_detail, name='topic_detail'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('myblog/', views.myblog, name='myblog'),

]
