from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('bienvenida/<str:tipo_doc>/<str:num_doc>/', views.bienvenida, name='bienvenida'),
    path('medicamentos/<str:tipo_doc>/<str:num_doc>/<str:departamento>/', views.medicamentos, name='medicamentos'),
    path('medicamentos/<str:tipo_doc>/<str:num_doc>/<str:departamento>/editar/<str:codigo>/', views.editar_medicamento, name='editar_medicamento'),
    path('medicamentos/<str:tipo_doc>/<str:num_doc>/<str:departamento>/eliminar/<str:codigo>/', views.eliminar_medicamento, name='eliminar_medicamento'),
]