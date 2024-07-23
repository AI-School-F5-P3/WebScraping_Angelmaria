from django.contrib import admin
from django.urls import path
from quotes import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.quote_list, name='quote_list'),
    path('author/<int:author_id>/', views.author_detail, name='author_detail'),
]
