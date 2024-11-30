from django.urls import path
from . import views

urlpatterns=[
    path('favorites/', views.get_favorites),
    path('favorites/create/', views.create_favorites),
    path('favorites/update/<int:favorite_pk>/', views.update_favorites),
    path('favorites/delete/<int:favorite_pk>/', views.delete_favorites),
    path('getbanks/', views.get_banks)
]