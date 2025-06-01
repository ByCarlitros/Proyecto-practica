from django.urls import path
from . import views

urlpatterns = [
    path('menu_usuario/', views.menu_usuario, name='menu_usuario'),
    path('menu_admin/', views.menu_admin, name='menu_admin'),
    path('actualizar_solicitud/', views.actualizar_solicitud, name='actualizar_solicitud'),
    path('menu_consolidado/', views.menu_consolidado, name='menu_consolidado'),  # Nueva vista
]
