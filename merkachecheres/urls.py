from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views




urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('categorias/', views.vercategorias, name='vercategorias'),
    path('chat/', views.chat, name='chat'),
    path('publicar/', views.publicar, name='publicar'),
    path('categoriaProducto/<int:categoria_id>/', views.categoria_producto, name='categoria_producto'),
    path('producto/<int:producto_id>/', views.producto, name='producto'),
    path('producto/', views.producto, name='producto'),
    path('logout/', views.logout, name='logout'),
    path('registro/', views.registro, name='registro'),
    path('completardatos/', views.completardatos, name='completardatos'),
    path('eliminar-imagen-producto/<int:imagen_id>/', views.eliminar_imagen_producto, name='eliminar_imagen_producto'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('cliente_dashboard/', views.cliente_dashboard, name='cliente_dashboard'),
    path('cambio-contrasena/', views.solicitar_cambio_contrasena, name='solicitar_cambio_contrasena'),
    path('restablecer-contrasena/', views.restablecer_contrasena, name='restablecer_contrasena'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
    path('todos-los-productos/', views.todos_los_productos, name='todos_los_productos'),
    path('agregar_al_carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('vaciar_carrito/', views.vaciar_carrito, name='vaciar_carrito'),
    path('eliminar_del_carrito/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('eliminar_usuario/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('editar_usuario/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('sobre_nosotros/', views.sobre_nosotros, name='sobre_nosotros'),
    path('perfil/', views.perfil, name='perfil'),
    path('eliminar_usuario/', views.eliminar_usuario, name='eliminar_usuario'),

    path("backup/", views.backup, name="backup"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)