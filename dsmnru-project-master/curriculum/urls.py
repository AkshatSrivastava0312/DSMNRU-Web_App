from django.urls import path
from . import views

app_name='curriculum'
urlpatterns = [
    path('', views.DepartmentListView.as_view(), name='department_list'),
    path('<slug:slug>/', views.SubjectListView.as_view(), name='subject_list'),
    path('<str:department>/<slug:slug>/', views.LessonListView.as_view(), name='lesson_list'),
    path('<str:department>/<str:slug>/create/', views.LessonCreateView.as_view(),name='lesson_create'),
    path('<str:department>/<str:subject>/<slug:slug>/', views.LessonDetailView.as_view(),name='lesson_detail'),
    path('<str:department>/<str:subject>/<slug:slug>/update/', views.LessonUpdateView.as_view(),name='lesson_update'),
    path('<str:department>/<str:subject>/<slug:slug>/delete/', views.LessonDeleteView.as_view(),name='lesson_delete'),

]
