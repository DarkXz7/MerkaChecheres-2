import os
from .models import Usuario, Producto, ImagenProducto
from .models import *
from django.shortcuts import render, redirect
from django.contrib import messages
from decimal import Decimal, InvalidOperation
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from decimal import Decimal, InvalidOperation
from .colombia_data import DEPARTAMENTOS_Y_MUNICIPIOS
from django.contrib.messages import get_messages
from django.core.paginator import Paginator
from django.shortcuts import redirect, get_object_or_404
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from PIL import Image

def registro(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')  # Contraseña sin encriptar
        telefono = request.POST.get('telefono')
        departamento = request.POST.get('departamento')
        direccion = request.POST.get('direccion')
        municipio = request.POST.get('municipio', 'Sin municipio')
        foto_perfil = request.FILES.get('foto_perfil')

        # Validar que los campos no estén vacíos
        if not full_name or not email or not username or not password:
            messages.error(request, "Todos los campos son obligatorios.")
            return render(request, 'registro.html')

        # Validar que el correo electrónico y el nombre de usuario sean únicos
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "El correo electrónico no es válido.")
            return render(request, 'registro.html')
        
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
                password=password,  # Guardar la contraseña sin encriptar
                telefono=telefono,
                departamento=departamento,
                direccion=direccion,
                municipio=municipio,
                foto_perfil=foto_perfil
            )
            usuario.save()

            # Autenticación: Crear la variable de sesión automáticamente
            request.session["validar"] = {
                "id": usuario.id,
                "rol": usuario.rol,
                "nombre": usuario.full_name
            }

            messages.success(request, f"Tu cuenta ha sido creada exitosamente. ¡Bienvenido a MerkaChecheres {usuario.full_name}!")
            return redirect("index")

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
    # Validar resolución de la imagen
    try:
        image = Image.open(value)
        if image.width < 300 or image.height < 300:
            raise ValidationError("La imagen debe tener mínimo 300x300 píxeles y ser de buena calidad.")
    except Exception:
        raise ValidationError("No se pudo procesar la imagen. Asegúrate de que sea válida y de al menos 300x300 píxeles.")

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
    from .models import Categoria  #importar Categoria
    categorias = Categoria.objects.all()  # Obtener todas las categorías

    usuario_id = request.session.get('validar', {}).get('id')
    usuario_actual = Usuario.objects.get(id=usuario_id) if usuario_id else None

    if not usuario_actual:
        messages.error(request, "Debes iniciar sesión para publicar un producto.")
        return redirect('login')

    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        precio_raw = request.POST.get('precio')
        categoria = request.POST.get('categoria')
        descripcion = request.POST.get('descripcion')
        imagenes = request.FILES.getlist('imagen')  # Capturar múltiples imágenes
        marca = request.POST.get('marca')
        descuento = request.POST.get('descuento')
        dimensiones = request.POST.get('dimensiones')
        stock = request.POST.get('Stock')  # Obtener el valor de stock del formulario
        usuario_id = request.session.get('validar', {}).get('id')
        usuario_actual = Usuario.objects.get(id=usuario_id) if usuario_id else None


        # Validar que el titulo tenga al menos 5 caracteres
        if len(titulo.strip()) < 5:
            messages.error(request, "El título debe tener al menos 5 caracteres.")

        # Validar que no se suban más de 12 imágenes
        if len(imagenes) > 12:
            messages.error(request, "Solo puedes subir un máximo de 12 imágenes.")

        # Validar campos obligatorios
        if not titulo:
            messages.error(request, "El campo 'Título' es obligatorio.")

            
        if not precio_raw:
            messages.error(request, "El campo 'Precio' es obligatorio.")
        try:
        # Si el precio viene con comas o puntos como separadores
            if isinstance(precio_raw, str):
                precio = Decimal(precio_raw.replace(',', '').replace('.', '')) / 100
            else:
                precio = Decimal(precio_raw)

            if precio <= 0:
                messages.error(request, "El precio debe ser mayor a 0.")
        except (InvalidOperation, AttributeError, TypeError):
            messages.error(request, "El campo Precio debe ser un número válido.")


        if not categoria:
            messages.error(request, "El campo 'Categoría' es obligatorio.")
        if not descripcion:
            messages.error(request, "El campo 'Descripción' es obligatorio.")
        if not stock:
            messages.error(request, "El campo 'Stock' es obligatorio.")
        

        # Si hay errores, no continuar
        if len(list(messages.get_messages(request))) > 0:
            return render(request, 'publicarArticulo.html', {'categorias': categorias})

        # Validar que todos los archivos sean imágenes válidas
        for imagen in imagenes:
            try:
                validar_extension_imagen(imagen)  # Usa el validador definido en el modelo
            except ValidationError as e:
                messages.error(request, f"El Archivo {imagen.name} no es válido. {e}")
                return render(request, 'publicarArticulo.html', {'categorias': categorias})

        # Si hay errores, no continuar
        if len(list(messages.get_messages(request))) > 0:
            return render(request, 'publicarArticulo.html', {'categorias': categorias})

        try:
            # Convertir categoría a entero
            categoria = int(categoria)

            # Convertir precio a Decimal
            

            # Procesar descuento (si existe)
            if descuento:
                descuento = Decimal(descuento.replace('%', '').strip())
            else:
                descuento = None

            # Validar y convertir stock a entero
            try:
                stock = int(stock)

                if stock < 0:
                    raise ValueError("El stock no puede ser negativo.")
                elif stock == 0:
                    messages.error(request, "El stock no puede ser 0. Debes haber al menos una unidad disponible.")
                    return render(request, 'publicarArticulo.html', {'categorias': categorias})
                elif stock > 10000:
                    messages.error(request, "El stock no puede superar las 10.000 unidades.")
                    return render(request, 'publicarArticulo.html', {'categorias': categorias})
            except ValueError:
                messages.error(request, "El campo Stock debe ser un número entero válido.")
                return render(request, 'publicarArticulo.html', {'categorias': categorias})
            

            # Guardar producto
            categoria_obj = Categoria.objects.get(id=categoria) if categoria else None
            producto = Producto(
                titulo=titulo,
                precio=precio,
                categoria=categoria_obj,
                descripcion=descripcion,
                marca=marca,
                descuento=descuento,
                dimensiones=dimensiones,
                stock=stock,
                vendedor=usuario_actual
            )
            producto.save()

            # Guardar las imágenes relacionadas
            for imagen in imagenes:
                ImagenProducto.objects.create(producto=producto, imagen=imagen)

            messages.success(request, "Producto publicado exitosamente")
            return render(request, 'publicarArticulo.html', {'redirect': True, 'categorias': categorias})

        except InvalidOperation:
            messages.error(request, "Error: Ingrese un precio válido.")
            return render(request, 'publicarArticulo.html', {'categorias': categorias})

        except Exception as e:
            messages.error(request, f"Error al guardar el producto: {e}")
            return render(request, 'publicarArticulo.html', {'categorias': categorias})

    # Para GET o si no hay POST, también envía las categorías
    return render(request, 'publicarArticulo.html', {'categorias': categorias})


def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    # Obtén el carrito de la sesión o inicialízalo
    carrito = request.session.get('carrito', {})

    # Obtén la cantidad seleccionada desde el formulario
    cantidad_seleccionada = int(request.POST.get('cantidad', 1))

    imagen_url = ""
    primera_imagen = producto.imagenes.first()
    if primera_imagen and primera_imagen.imagen:
        imagen_url = primera_imagen.imagen.url
    # Si el producto ya está en el carrito, incrementa la cantidad
    if str(producto_id) in carrito:
        carrito[str(producto_id)]['cantidad'] += cantidad_seleccionada
    else:
        # Agrega el producto al carrito
        carrito[str(producto_id)] = {
            'titulo': producto.titulo,
            'precio': float(producto.precio),
            'categoria': producto.categoria.nombre if producto.categoria else 'Sin categoría',
            'stock': producto.stock,
            'cantidad': cantidad_seleccionada,
            'imagen_url': imagen_url
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
    from .models import Categoria  # Asegúrar de importar Categoria si no lo tiene arriba

    usuario_id = request.session.get('validar', {}).get('id')

    if not usuario_id:
        messages.error(request, "No has iniciado sesión.")
        return redirect('login')

    usuario = Usuario.objects.get(id=usuario_id)
    municipios = DEPARTAMENTOS_Y_MUNICIPIOS.get(usuario.departamento, [])

    # Mostrar productos publicados si se solicita
    mostrar_mis_productos = request.GET.get('mis_productos') == '1'
    productos_usuario = Producto.objects.filter(vendedor=usuario) if mostrar_mis_productos else None

    # Lógica para mostrar y editar un producto publicado en la misma vista
    producto_a_editar = None
    editar_producto_id = request.GET.get('editar_producto')
    eliminar_producto_id = request.GET.get('eliminar_producto')
    if mostrar_mis_productos and editar_producto_id:
        try:
            producto_a_editar = Producto.objects.get(id=editar_producto_id, vendedor=usuario)
        except Producto.DoesNotExist:
            producto_a_editar = None

    # Eliminar producto
    if mostrar_mis_productos and eliminar_producto_id:
        try:
            producto_a_eliminar = Producto.objects.get(id=eliminar_producto_id, vendedor=usuario)
            producto_a_eliminar.delete()
            messages.success(request, "Producto eliminado correctamente.")
            return redirect(f"{request.path}?mis_productos=1")
        except Producto.DoesNotExist:
            messages.error(request, "El producto no existe o no tienes permiso para eliminarlo.")

    # Si se envía el formulario de edición de producto
    if request.method == 'POST' and request.POST.get('producto_id'):
        producto_id = request.POST.get('producto_id')
        producto = Producto.objects.get(id=producto_id, vendedor=usuario)
        producto.titulo = request.POST.get('titulo')
        producto.descripcion = request.POST.get('descripcion')
        # Validar y convertir precio
        try:
            producto.precio = Decimal(request.POST.get('precio'))
        except (InvalidOperation, TypeError):
            messages.error(request, "El precio debe ser un número válido.")
            return render(request, 'editar.html', {
                'usuario': usuario,
                'departamentos': DEPARTAMENTOS_Y_MUNICIPIOS.keys(),
                'departamentos_y_municipios': DEPARTAMENTOS_Y_MUNICIPIOS,
                'municipios': municipios,
                'mostrar_mis_productos': mostrar_mis_productos,
                'productos_usuario': productos_usuario,
                'producto_a_editar': producto,
                'categorias': Categoria.objects.all(),
            })
        # Otros campos
        categoria_id = request.POST.get('categoria')
        producto.categoria = Categoria.objects.get(id=categoria_id) if categoria_id else None
        producto.marca = request.POST.get('marca')
        producto.dimensiones = request.POST.get('dimensiones')
        producto.stock = request.POST.get('stock')
        # Validar y convertir descuento
        descuento = request.POST.get('descuento')
        if descuento:
            try:
                producto.descuento = Decimal(descuento)
            except (InvalidOperation, TypeError):
                messages.error(request, "El descuento debe ser un número válido.")
                return render(request, 'editar.html', {
                    'usuario': usuario,
                    'departamentos': DEPARTAMENTOS_Y_MUNICIPIOS.keys(),
                    'departamentos_y_municipios': DEPARTAMENTOS_Y_MUNICIPIOS,
                    'municipios': municipios,
                    'mostrar_mis_productos': mostrar_mis_productos,
                    'productos_usuario': productos_usuario,
                    'producto_a_editar': producto,
                    'categorias': Categoria.objects.all(),
                })
        else:
            producto.descuento = None

        producto.save()
        messages.success(request, "Producto actualizado correctamente.")
        return redirect(f"{request.path}?mis_productos=1")

    # Si se envía el formulario de edición de usuario
    elif request.method == 'POST':
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
                'municipios': municipios,
                'mostrar_mis_productos': mostrar_mis_productos,
                'productos_usuario': productos_usuario,
                'producto_a_editar': producto_a_editar,
                'categorias': Categoria.objects.all(),
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
        'municipios': municipios,
        'mostrar_mis_productos': mostrar_mis_productos,
        'productos_usuario': productos_usuario,
        'producto_a_editar': producto_a_editar,
        'categorias': Categoria.objects.all(),
    })



def admin_dashboard(request):
    tabla = request.GET.get('tabla', 'usuarios')
    usuario_id = request.session.get('validar', {}).get('id')
    usuario_actual = Usuario.objects.get(id=usuario_id) if usuario_id else None

    usuarios_list = Usuario.objects.all().order_by('id')
    usuarios_paginator = Paginator(usuarios_list, 10)
    usuarios_page_number = request.GET.get('page') if tabla == 'usuarios' else 1
    usuarios = usuarios_paginator.get_page(usuarios_page_number)

    if tabla == 'productos':
        productos_list = Producto.objects.all().order_by('id')
        productos_paginator = Paginator(productos_list, 10)
        productos_page_number = request.GET.get('page')
        productos = productos_paginator.get_page(productos_page_number)
        context = {
            'mostrar_productos': True,
            'productos': productos,
            'usuarios': usuarios,  # SIEMPRE ENVIAR USUARIOS
            'usuario_actual': usuario_actual,
            'total_productos': Producto.objects.count(),
        }
    else:
        context = {
            'mostrar_productos': False,
            'usuarios': usuarios,
            'usuario_actual': usuario_actual,
            'total_productos': Producto.objects.count(),
        }

    return render(request, 'admin.html', context)
    
def cliente_dashboard(request):    
    return render(request, 'index.html')
def vendedor_dashboard(request):
    return render(request, 'vendedor.html')
def producto(request, producto_id):
    try:
        # Buscar el producto por su ID
        producto = Producto.objects.get(id=producto_id)
        imagenes = producto.imagenes.all()  # Obtener las imágenes relacionadas

        productos_vendedor = Producto.objects.filter(vendedor=producto.vendedor).exclude(id=producto_id)

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
        'productos_vendedor': productos_vendedor,
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

def vercategorias(request):
    return render(request, "categorias.html")

def categoriaProducto(request):
    return render(request, "categoriaProducto.html")




def categoria_producto(request, categoria_id):
    # Diccionario de categorías
    categorias = {
        1: 'Electrónica',
        2: 'Ropa y Accesorios',
        3: 'Hogar y Jardín',
        4: 'Ferretería',
        5: 'Libros y Papelería',
        6: 'Belleza y Cuidado Personal',
        7: 'Juguetes',
        8: 'Deporte',
        9: 'Vehículos',
    }

    # Obtener el nombre de la categoría
    categoria_nombre = categorias.get(categoria_id, 'Categoría desconocida')

    # Filtrar productos por la categoría seleccionada
    productos = Producto.objects.filter(categoria=categoria_id)

    carrito = request.session.get('carrito', {})
    usuario = request.session.get('validar', None)
    return render(request, 'categoriaProducto.html', {
        'categoria': categoria_nombre,
        'productos': productos,
        'carrito': carrito,
        'usuario': usuario,

    })

def admin_dashboard(request):
    tabla = request.GET.get('tabla', 'usuarios')
    categoria_seleccionada = request.GET.get('categoria')  # Obtener la categoría seleccionada
    usuario_id = request.session.get('validar', {}).get('id')
    usuario_actual = Usuario.objects.get(id=usuario_id) if usuario_id else None

    # Paginación de usuarios
    usuarios_list = Usuario.objects.all().order_by('id')
    usuarios_paginator = Paginator(usuarios_list, 10)
    usuarios_page_number = request.GET.get('page') if tabla == 'usuarios' else 1
    usuarios = usuarios_paginator.get_page(usuarios_page_number)

    # Lógica para editar productos
    editar_producto_id = request.GET.get('editar_producto')
    producto_a_editar = None

    if editar_producto_id:
        producto_a_editar = Producto.objects.get(id=editar_producto_id)

        if request.method == 'POST':
            # Validar y guardar el producto
            try:
                producto_a_editar.titulo = request.POST.get('titulo')
                categoria_id = request.POST.get('categoria')
                producto_a_editar.categoria = Categoria.objects.get(id=categoria_id) if categoria_id else None
                producto_a_editar.descripcion = request.POST.get('descripcion')
                producto_a_editar.marca = request.POST.get('marca')
                producto_a_editar.dimensiones = request.POST.get('dimensiones')
                producto_a_editar.stock = int(request.POST.get('stock', 0))

                # Validar precio
                try:
                    producto_a_editar.precio = Decimal(request.POST.get('precio'))
                except (InvalidOperation, TypeError):
                    messages.error(request, "El precio debe ser un número válido.")
                    return render(request, 'admin.html', {
                        'producto_a_editar': producto_a_editar,
                        'mostrar_productos': True,
                        'categorias': Categoria.objects.all(),
                        'usuarios': Usuario.objects.all(),
                        'usuario_actual': Usuario.objects.get(id=request.session.get('validar', {}).get('id')),
                    })

                # Validar descuento
                descuento = request.POST.get('descuento')
                if descuento:
                    try:
                        producto_a_editar.descuento = Decimal(descuento)
                    except (InvalidOperation, TypeError):
                        messages.error(request, "El descuento debe ser un número válido.")
                        return render(request, 'admin.html', {
                            'producto_a_editar': producto_a_editar,
                            'mostrar_productos': True,
                            'categorias': Categoria.objects.all(),
                            'usuarios': Usuario.objects.all(),
                            'usuario_actual': Usuario.objects.get(id=request.session.get('validar', {}).get('id')),
                        })
                else:
                    producto_a_editar.descuento = None

                # Guardar el producto si no hay errores
                producto_a_editar.save()
                messages.success(request, f"El producto '{producto_a_editar.titulo}' se ha actualizado correctamente.")
                return redirect(f"{request.path}?tabla=productos")

            except Exception as e:
                messages.error(request, f"Hubo un error al actualizar el producto: {str(e)}")
                return render(request, 'admin.html', {
                    'producto_a_editar': producto_a_editar,
                    'mostrar_productos': True,
                    'categorias': Categoria.objects.all(),
                    'usuarios': Usuario.objects.all(),
                    'usuario_actual': Usuario.objects.get(id=request.session.get('validar', {}).get('id')),
                })


    if request.method == 'POST' and tabla == 'categorias':
        accion = request.POST.get('accion_categoria')
        if accion == 'agregar':
            nombre = request.POST.get('nombre_categoria')
            if nombre:
                Categoria.objects.create(nombre=nombre)
                messages.success(request, "Categoría agregada correctamente.")
        elif accion == 'eliminar':
            categoria_id = request.POST.get('categoria_id')
            if categoria_id:
                Categoria.objects.filter(id=categoria_id).delete()
                messages.success(request, "Categoría eliminada correctamente.")
        return redirect(f"{request.path}?tabla=categorias")


    #logica para la paginación de productos
    # Paginación de productos
    if tabla == 'productos':
        if categoria_seleccionada:
            productos_list = Producto.objects.filter(categoria_id=categoria_seleccionada).order_by('id')
        else:
            productos_list = Producto.objects.all().order_by('id')
        productos_paginator = Paginator(productos_list, 10)
        productos_page_number = request.GET.get('page')
        productos = productos_paginator.get_page(productos_page_number)
        context = {
            'mostrar_productos': True,
            'productos': productos,
            'usuarios': usuarios,
            'usuario_actual': usuario_actual,
            'total_productos': Producto.objects.count(),
            'producto_a_editar': producto_a_editar,
            'categorias': Categoria.objects.all(),
            'categoria_seleccionada': categoria_seleccionada,
            
        }

    elif tabla == 'categorias':
        # Lógica para las categorías
        categorias_list = Categoria.objects.all().order_by('id')
        categorias_paginator = Paginator(categorias_list, 10)
        categorias_page_number = request.GET.get('page')
        categorias = categorias_paginator.get_page(categorias_page_number)
        context = {
            'mostrar_categorias': True,
            'categorias': categorias,
            'usuarios': usuarios,
            'usuario_actual': usuario_actual,
        }

    else:
        context = {
            'mostrar_usuarios': True,  # <-- AGREGA ESTA LÍNEA
            'usuarios': usuarios,
            'total_usuarios': usuarios.paginator.count,
            'usuario_actual': usuario_actual,
            'total_productos': Producto.objects.count(),
        }

    return render(request, 'admin.html', context)




def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        producto.titulo = request.POST.get('titulo')
        categoria_id = request.POST.get('categoria')
        producto.categoria = Categoria.objects.get(id=categoria_id) if categoria_id else None
        producto.descripcion = request.POST.get('descripcion')
        producto.marca = request.POST.get('marca')
        producto.dimensiones = request.POST.get('dimensiones')
        producto.stock = request.POST.get('stock')

        # Validar y convertir precio y descuento
        try:
            producto.precio = Decimal(request.POST.get('precio'))
        except (InvalidOperation, TypeError):
            messages.error(request, "El precio debe ser un número válido.")
            return render(request, 'editar_producto.html', {'producto': producto})

        descuento = request.POST.get('descuento')
        if descuento:
            try:
                producto.descuento = Decimal(descuento)
            except (InvalidOperation, TypeError):
                messages.error(request, "El descuento debe ser un número válido.")
                return render(request, 'editar_producto.html', {'producto': producto})
        else:
            producto.descuento = None

        producto.save()
        messages.success(request, "Producto actualizado exitosamente.")
        return redirect('admin_dashboard')

    return render(request, 'editar_producto.html', {
    'producto': producto,
    'categorias': Categoria.objects.all(),
})