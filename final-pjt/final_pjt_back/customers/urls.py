from django.urls import path
from . import views

urlpatterns=[
    path('qanda/', views.questions_list),
    path('qanda/category/', views.get_category),
    path('qanda/create/', views.question_create),
    path('qanda/update/<int:question_pk>/', views.question_update),
    path('qanda/delete/<int:question_pk>/', views.question_delete),
    path('qanda/<int:question_pk>/', views.question_detail), 
    path('qanda/<int:question_pk>/answer/create/', views.create_answer),
    path('qanda/<int:question_pk>/answer/', views.get_answer),


]

