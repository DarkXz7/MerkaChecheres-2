from django.contrib import admin
from .models import *
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe







class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'rol', 'password_field')  # Campos visibles en la lista

    def password_field(self, obj):
        # Muestra la contraseña encriptada con un botón para mostrar/ocultar
        return format_html(
            '''
            <input type="password" value="{}" id="password_field_{}" style="margin-right: 5px;" />
            <button type="button" onclick="togglePasswordVisibility('password_field_{}')">Mostrar</button>
            <script>
                function togglePasswordVisibility(fieldId) {{
                    const field = document.getElementById(fieldId);
                    const button = field.nextElementSibling;
                    if (field.type === "password") {{
                        field.type = "text";
                        button.innerText = "Ocultar";
                    }} else {{
                        field.type = "password";
                        button.innerText = "Mostrar";
                    }}
                }}
            </script>
            ''',
            obj.password,
            obj.id,
            obj.id
        )

    password_field.short_description = "Contraseña"




class ImagenProductoInline(admin.TabularInline):
    model = ImagenProducto
    extra = 1
    readonly_fields = ('imagen_preview',)
    fields = ('imagen_preview', 'imagen')

    def imagen_preview(self, obj):
        if obj.imagen:
            return format_html(f'<img src="{obj.imagen.url}" style="max-height: 200px; max-width: 200px;" />')
        return "No hay imagen disponible"

    imagen_preview.short_description = "Vista Previa"

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'precio', 'categoria', 'fecha_publicacion', 'imagen_principal')
    list_filter = ('categoria', 'fecha_publicacion')
    search_fields = ('titulo', 'descripcion')
    inlines = [ImagenProductoInline]

    def imagen_principal(self, obj):
        primera_imagen = obj.imagenes.first()
        if primera_imagen and primera_imagen.imagen:
            return format_html(f'<img src="{primera_imagen.imagen.url}" style="max-height: 100px; max-width: 100px;" />')
        return "Sin imagen"

    imagen_principal.short_description = "Imagen Principal"

admin.site.register(Producto, ProductoAdmin)
admin.site.register(ImagenProducto)
admin.site.register(Usuario, UsuarioAdmin)