from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_readlist),
    path('<int:todo_id>/', views.read_update_delete),
]