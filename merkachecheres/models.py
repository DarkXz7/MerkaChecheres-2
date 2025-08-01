from django.db import models
import os
from django.core.exceptions import ValidationError
# Create your models here.
from django.db import models

def validar_extension_imagen(value):
    ext = os.path.splitext(value.name)[1]  # Obtiene la extensión del archivo
    extensiones_validas = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
    if ext.lower() not in extensiones_validas:
        raise ValidationError(f'Extensión no válida: {ext}. Solo se permiten imágenes /n ({", ".join(extensiones_validas)}).')
    # No validar resolución si es la imagen por defecto
    if hasattr(value, 'name') and 'user_default' in value.name:
        return
    try:
        image = Image.open(value)
        if image.width < 300 or image.height < 300:
            raise ValidationError("La imagen debe tener mínimo 300x300 píxeles y ser de buena calidad.")
    except Exception:
        raise ValidationError("No se pudo procesar la imagen. Asegúrate de que sea válida y de al menos 300x300 píxeles.")

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128, blank=True, null=True) 
    telefono = models.CharField(max_length=15, default="Sin teléfono")  # Valor por defecto
    departamento = models.CharField(max_length=100, default="Sin departamento")  # Valor por defecto
    direccion = models.CharField(max_length=255, default="Sin dirección")  # Valor por defecto
    municipio = models.CharField(max_length=100, default="Sin municipio")  # Valor por defecto
    foto_perfil = models.ImageField(
        upload_to='usuarios/perfiles', 
        validators=[validar_extension_imagen], 
        blank=True, 
        null=True,
        default='usuarios/perfiles/user_default.jpg',
        verbose_name="Ruta de la imagen de perfil"
    )  #
    ROLES = (
        (1, "Admin"),
        (2, "Cliente"),
        (3, "Vendedor")
    )
    rol = models.IntegerField(choices=ROLES, default=2)
    
    def __str__(self):
        return self.username





    
class Producto(models.Model):
    titulo = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    dimensiones = models.CharField(max_length=100, null=True, blank=True)
    stock = models.IntegerField()
    marca = models.CharField(max_length=100, null=True, blank=True)
    vendido = models.BooleanField(default=False)
    vendedor = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name='productos', 
        null=True,  # Permitir valores nulos temporalmente
        blank=True  # Permitir que el formulario no requiera este campo
    )
    
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    descripcion = models.TextField()
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='productos/imagenes', validators=[validar_extension_imagen])
    
    def __str__(self):
        return f"Imagen de {self.producto.titulo}"
    

class Carrito(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='carritos')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='carritos')
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Carrito de {self.usuario.username} - {self.producto.titulo} (Cantidad: {self.cantidad})"
    
class Reseña(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='resenas')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    texto = models.TextField()
    estrellas = models.PositiveSmallIntegerField(default=5)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.producto.titulo} ({self.estrellas} estrellas)"
    
    
    
class MensajeChat(models.Model):
    emisor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='mensajes_enviados')
    receptor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='mensajes_recibidos')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='mensajes_chat')
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.emisor.username} -> {self.receptor.username}: {self.texto[:20]}"
    
    
class Notificacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    otro_usuario = models.ForeignKey(Usuario, related_name='notificaciones_otro', on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, default='chat')
    leida = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)