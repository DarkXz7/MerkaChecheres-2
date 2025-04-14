from django.shortcuts import render, redirect
from .models import Usuario
from .models import Producto, ImagenProducto
from django.contrib import messages
from decimal import Decimal, InvalidOperation
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from decimal import Decimal
from .colombia_data import DEPARTAMENTOS_Y_MUNICIPIOS
from django.contrib.messages import get_messages
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import Producto, Carrito
import os
def registro(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        telefono = request.POST.get('telefono')
        departamento = request.POST.get('departamento')
        direccion = request.POST.get('direccion')
        municipio = request.POST.get('municipio', 'Sin municipio')
        
        
        
        
        # Validar que los campos no estén vacíos
        if not full_name or not email or not username or not password:
            messages.error(request, "Todos los campos son obligatorios.")
            return render(request, 'registro.html')

        # Validar que el correo electrónico y el nombre de usuario sean únicos
        if Usuario.objects.filter(email=email).exists():
            messages.error(request, "El correo electrónico ya está registrado.")
            return render(request, 'registro.html')

        if Usuario.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está registrado.")
            return render(request, 'registro.html')

        # Crear el usuario y guardarlo en la base de datos
        try:
            usuario = Usuario(
                full_name=full_name,
                email=email, 
                username=username, 
                password=password,
                telefono=telefono, 
                departamento=departamento, 
                direccion=direccion, 
                municipio=municipio, 
                
                )
            usuario.save()
            
            
            # Try to authenticate the newly created user
            try:
                q = Usuario.objects.get(email=email, password=password)
                # Autenticación: Creamos la variable de sesión
                request.session["pista"] = {
                    "id": q.id,
                    "rol": q.rol,
                    "nombre": q.full_name  # Changed from q.nombre to match the field name
                }
                messages.success(request, f"Tu cuenta ha sido creada exitosamente. ¡Bienvenido a MerkaChecheres {q.full_name}!")
                return redirect("index")
            except Usuario.DoesNotExist:
                request.session["pista"] = None
                messages.error(request, "Error en el autologin después del registro")
                return redirect('index')
        
        except Exception as e:
            messages.error(request, f"Error al guardar el usuario: {e}")
            return render(request, 'registro.html')
    return render(request, 'registro.html')
        

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            usuario = Usuario.objects.get(email=email, password=password)
            # Crear una sesión para el usuario
            request.session["validar"] = {
                "id": usuario.id,
                "rol": usuario.rol,
                "nombre": usuario.full_name
            }
            
            # Redirigir según el rol del usuario
            if usuario.rol == 1:  # Admin
                return redirect('admin_dashboard')
            elif usuario.rol == 2:  # Cliente
                return redirect('index')  # Redirige a la vista `index`
            elif usuario.rol == 3:  # Vendedor
                return redirect('index')

        except Usuario.DoesNotExist:
            messages.error(request, "Correo electrónico o contraseña incorrectos.")
            return render(request, 'login.html')
    return render(request, 'login.html')


def validar_extension_imagen(value):
    ext = os.path.splitext(value.name)[1]  # Obtiene la extensión del archivo
    extensiones_validas = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
    if ext.lower() not in extensiones_validas:
        raise ValidationError(f'Extensión no válida: {ext}. Solo se permiten imágenes ({", ".join(extensiones_validas)}).')


def sobre_nosotros(request):
    return render(request, 'sobre.html')


def eliminar_usuario(request, usuario_id):
    try:
        usuario = Usuario.objects.get(id=usuario_id)
        usuario.delete()
        messages.error(request, f"El usuario {usuario.full_name} ha sido eliminado exitosamente.")
    except Usuario.DoesNotExist:
        messages.error(request, "El usuario no existe.")
    return redirect('admin_dashboard')

def editar_usuario(request, usuario_id):
    try:
        usuario = Usuario.objects.get(id=usuario_id)

        if request.method == 'POST':
            usuario.full_name = request.POST.get('full_name')
            usuario.email = request.POST.get('email')
            usuario.username = request.POST.get('username')
            usuario.telefono = request.POST.get('telefono')
            usuario.departamento = request.POST.get('departamento')
            usuario.direccion = request.POST.get('direccion')
            usuario.municipio = request.POST.get('municipio')
            usuario.rol = request.POST.get('rol')

            nueva_contrasena = request.POST.get('password')
            if nueva_contrasena:
                usuario.password = make_password(nueva_contrasena)  # Encriptar la contraseña

            usuario.save()
            

            messages.success(request, f"El usuario {usuario.full_name} ha sido actualizado exitosamente.")
            return redirect('admin_dashboard')

        return render(request, 'editar_usuario.html', {'usuario': usuario})
    except Usuario.DoesNotExist:
        messages.error(request, "El usuario no existe.")
        return redirect('admin_dashboard')
    


from decimal import Decimal, InvalidOperation
import re

def publicar(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        precio = request.POST.get('precio')
        categoria = request.POST.get('categoria')
        descripcion = request.POST.get('descripcion')
        imagenes = request.FILES.getlist('imagen')  # Capturar múltiples imágenes
        marca = request.POST.get('marca')
        descuento = request.POST.get('descuento')
        dimensiones = request.POST.get('dimensiones')
        stock = request.POST.get('Stock')  # Obtener el valor de stock del formulario

        # Validar que no se suban más de 12 imágenes
        if len(imagenes) > 12:
            messages.error(request, "Solo puedes subir un máximo de 12 imágenes.")

        # Validar campos obligatorios
        if not titulo:
            messages.error(request, "El campo 'Título' es obligatorio.")
        if not precio:
            messages.error(request, "El campo 'Precio' es obligatorio.")
        if not categoria:
            messages.error(request, "El campo 'Categoría' es obligatorio.")
        if not descripcion:
            messages.error(request, "El campo 'Descripción' es obligatorio.")
        if not stock:
            messages.error(request, "El campo 'Stock' es obligatorio.")

        # Si hay errores, no continuar
        if len(list(messages.get_messages(request))) > 0:
            return render(request, 'publicarArticulo.html')

        # Validar que todos los archivos sean imágenes válidas
        for imagen in imagenes:
            try:
                validar_extension_imagen(imagen)  # Usa el validador definido en el modelo
            except ValidationError as e:
                messages.error(request, f"El Archivo {imagen.name} no es válido. {e}")
                return render(request, 'publicarArticulo.html')

        # Si hay errores, no continuar
        if len(list(messages.get_messages(request))) > 0:
            return render(request, 'publicarArticulo.html')


        try:
            # Convertir categoría a entero
            categoria = int(categoria)

            # Convertir precio a Decimal
            precio = Decimal(precio.replace(',', '').replace('.', '')) / 100

            # Procesar descuento (si existe)
            if descuento:
                descuento = Decimal(descuento.replace('%', '').strip())

            # Validar y convertir stock a entero
            try:
                stock = int(stock)
                if stock < 0:
                    raise ValueError("El stock no puede ser negativo.")
            except ValueError:
                messages.error(request, "El campo Stock debe ser un número entero válido.")
                return render(request, 'publicarArticulo.html')

            # Guardar producto
            producto = Producto(
                titulo=titulo,
                precio=precio,
                categoria=categoria,
                descripcion=descripcion,
                marca=marca,
                descuento=descuento,
                dimensiones=dimensiones,
                stock=stock  # Asignar el valor de stock
            )
            producto.save()

            # Guardar las imágenes relacionadas
            for imagen in imagenes:
                ImagenProducto.objects.create(producto=producto, imagen=imagen)

            messages.success(request, "Producto publicado exitosamente")
            return render(request, 'publicarArticulo.html', {'redirect': True})

        except InvalidOperation:
            messages.error(request, "Error: Ingrese un precio válido.")
            return render(request, 'publicarArticulo.html')

        except Exception as e:
            messages.error(request, f"Error al guardar el producto: {e}")
            return render(request, 'publicarArticulo.html')

    return render(request, 'publicarArticulo.html')


def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    # Obtén el carrito de la sesión o inicialízalo
    carrito = request.session.get('carrito', {})

    # Obtén la cantidad seleccionada desde el formulario
    cantidad_seleccionada = int(request.POST.get('cantidad', 1))

    # Si el producto ya está en el carrito, incrementa la cantidad
    if str(producto_id) in carrito:
        carrito[str(producto_id)]['cantidad'] += cantidad_seleccionada
    else:
        # Agrega el producto al carrito
        carrito[str(producto_id)] = {
            'titulo': producto.titulo,
            'precio': float(producto.precio),
            'categoria': producto.get_categoria_display(),
            'stock': producto.stock,
            'cantidad': cantidad_seleccionada
        }

    # Guarda el carrito en la sesión
    request.session['carrito'] = carrito
    request.session.modified = True

    # Mensaje de éxito
    messages.success(request, f"{producto.titulo} se ha agregado al carrito.")
    return redirect('producto', producto_id=producto_id)





def solicitar_cambio_contrasena(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        # Verificar si el correo existe en la base de datos
        try:
            usuario = Usuario.objects.get(email=email)
            # Guardar el email en la sesión para usarlo en la siguiente vista
            request.session['email_para_cambio'] = email
            messages.success(request, "Correo verificado, Ahora puedes reestablecer tu contraseña")
            return redirect('restablecer_contrasena')  # Redirige al formulario de restablecimiento
        except Usuario.DoesNotExist:
            messages.error(request, "El correo electrónico no está registrado.")
            return render(request, 'solicitar_cambio_contrasena.html')

    return render(request, 'solicitar_cambio_contrasena.html')


def restablecer_contrasena(request):
    # Verificar si el email está en la sesión
    email = request.session.get('email_para_cambio')
    if not email:
        messages.error(request, "No se ha verificado ningún correo electrónico.")
        return redirect('solicitar_cambio_contrasena')

    try:
        usuario = Usuario.objects.get(email=email)

        if request.method == 'POST':
            nueva_contrasena = request.POST.get('password')
            confirmar_contrasena = request.POST.get('confirm_password')

            # Validar que las contraseñas coincidan
            if nueva_contrasena != confirmar_contrasena:
                messages.error(request, "Las contraseñas no coinciden.")
                return render(request, 'restablecer_contrasena.html')

            # Actualizar la contraseña del usuario
            usuario.password = (nueva_contrasena)  # Encripta la contraseña
            usuario.save()

            # Eliminar el email de la sesión
            del request.session['email_para_cambio']

            # Mostrar mensaje de éxito y redirigir al login
            messages.success(request, "Tu contraseña ha sido restablecida exitosamente Ahora puedes iniciar sesión.")
            return redirect('login')

        return render(request, 'restablecer_contrasena.html')

    except Usuario.DoesNotExist:
        messages.error(request, "El correo electrónico no es válido.")
        return redirect('solicitar_cambio_contrasena')

def eliminar_del_carrito(request, producto_id):
    # Obtén el carrito de la sesión
    carrito = request.session.get('carrito', {})

    # Elimina el producto del carrito si existe
    if str(producto_id) in carrito:
        del carrito[str(producto_id)]
        request.session['carrito'] = carrito
        request.session.modified = True
        messages.success(request, "El producto ha sido eliminado del carrito.")
    else:
        messages.error(request, "El producto no está en el carrito.")

    return redirect('index')  # Redirige al índice o a la página que prefieras

def logout(request):
    # Elimina la sesión del usuario
    request.session.flush()
    messages.success(request, "Has cerrado sesión exitosamente")
    return redirect('index')



def editar_perfil(request):
    usuario_id = request.session.get('validar', {}).get('id')

    if not usuario_id:
        messages.error(request, "No has iniciado sesión.")
        return redirect('login')

    usuario = Usuario.objects.get(id=usuario_id)
    municipios = DEPARTAMENTOS_Y_MUNICIPIOS.get(usuario.departamento, [])

    if request.method == 'POST':
        # Obtener los datos del formulario
        full_name = request.POST.get('nombreApellido')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        departamento = request.POST.get('departamento')
        municipio = request.POST.get('municipio')
        nueva_contrasena = request.POST.get('password')

        # Validar que los campos requeridos no estén vacíos
        if not full_name or not email or not telefono or not direccion or not departamento or not municipio:
            messages.error(request, "Todos los campos son obligatorios")
            return render(request, 'editar.html', {
                'usuario': usuario,
                'departamentos': DEPARTAMENTOS_Y_MUNICIPIOS.keys(),
                'departamentos_y_municipios': DEPARTAMENTOS_Y_MUNICIPIOS,
                'municipios': municipios
            })

        # Actualizar los datos del usuario
        usuario.full_name = full_name
        usuario.email = email
        usuario.telefono = telefono
        usuario.direccion = direccion
        usuario.departamento = departamento
        usuario.municipio = municipio

        # Actualizar la contraseña si se proporciona una nueva
        if nueva_contrasena and nueva_contrasena.strip():
            usuario.password = nueva_contrasena

        usuario.save()

        messages.success(request, "Perfil actualizado exitosamente.")
        return redirect('index')

    return render(request, 'editar.html', {
        'usuario': usuario,
        'departamentos': DEPARTAMENTOS_Y_MUNICIPIOS.keys(),
        'departamentos_y_municipios': DEPARTAMENTOS_Y_MUNICIPIOS,
        'municipios': municipios
    })



def admin_dashboard(request):
    usuarios = Usuario.objects.all()
    return render(request, 'admin.html', {'usuarios': usuarios})
    
def cliente_dashboard(request):    
    return render(request, 'index.html')
def vendedor_dashboard(request):
    return render(request, 'vendedor.html')
def producto(request, producto_id):
    try:
        # Buscar el producto por su ID
        producto = Producto.objects.get(id=producto_id)
        imagenes = producto.imagenes.all()  # Obtener las imágenes relacionadas

        # Calcular el total del carrito
        carrito = request.session.get('carrito', {})
        total_carrito = sum(item['precio'] * item['cantidad'] for item in carrito.values())

    except Producto.DoesNotExist:
        # Si el producto no existe, redirigir al índice con un mensaje de error
        messages.error(request, "El producto no existe.")
        return redirect('index')

    return render(request, 'producto.html', {
        'producto': producto,
        'imagenes': imagenes,
        'total_carrito': total_carrito,  # Pasa el total al contexto
    })

def producto_view(request):
    # Example context data
    context = {
        'producto': {
            'titulo': 'Sample Product',
        },
        'imagenes': [],  # Add your image data here
    }
    return render(request, 'producto.html', context)


def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'producto.html', {'producto': producto})


def index(request):
    """
    Vista para la página principal (index) de la aplicación.
    Esta vista obtiene productos, verifica si hay una sesión activa y calcula el total del carrito.
    """

    # 1. Obtener productos disponibles
    # Se seleccionan 5 productos aleatorios de la base de datos para mostrarlos en la página principal.
    productos = Producto.objects.order_by('?')[:5]

    # 2. Verificar si hay una sesión activa
    # Se intenta obtener la información de la sesión del usuario desde `request.session`.
    sesion_activa = request.session.get('validar', None)
    usuario = None  # Inicializa el usuario como `None` por defecto.

    if sesion_activa:
        # Si hay una sesión activa, se obtiene el ID del usuario desde la sesión.
        usuario_id = sesion_activa.get('id')
        # Se busca el usuario en la base de datos utilizando el ID.
        usuario = Usuario.objects.get(id=usuario_id)

    # 3. Obtener el carrito de la sesión
    # Se obtiene el carrito almacenado en la sesión. Si no existe, se inicializa como un diccionario vacío.
    carrito = request.session.get('carrito', {})

    # 4. Calcular el total del carrito
    # Se calcula el total del carrito sumando el precio de cada producto multiplicado por su cantidad.
    total_carrito = sum(item['precio'] * item['cantidad'] for item in carrito.values())

    # 5. Renderizar la plantilla `index.html`
    # Se pasa el contexto a la plantilla para que pueda mostrar los datos necesarios.
    return render(request, "index.html", {
        'productos': productos,  # Lista de productos seleccionados aleatoriamente.
        'productos_count': productos.count(),  # Cantidad de productos seleccionados.
        'total_carrito': total_carrito,  # Total del carrito (precio total de los productos en el carrito).
        'usuario': usuario,  # Objeto del usuario autenticado (si hay sesión activa).
    })
    
def vaciar_carrito(request):
    # Limpia los mensajes existentes
    
    storage = get_messages(request)
    for _ in storage:
        pass  # Esto consume los mensajes existentes y los elimina

    # Vacía el carrito
    request.session['carrito'] = {}
    request.session.modified = True
    
    # Agrega el mensaje de que el carrito fue vaciado
    messages.success(request, " Tu carrito ha sido vaciado")
    return redirect('index')


def adminlogin(request):
    return render(request, "adminlogin.html")

def completardatos(request):
    return render(request, "completardatos.html")