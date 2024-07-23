from django.urls import path
from . import views

urlpatterns = [
    path('', views.quote_list, name='quote_list'),
    path('author/<int:author_id>/', views.author_detail, name='author_detail'),
]
