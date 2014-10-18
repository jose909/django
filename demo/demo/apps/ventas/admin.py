from django.contrib import admin
from demo.apps.ventas.models import cliente,producto
from demo.apps.ventas.models import categoriaProducto

class productoAdmin(admin.ModelAdmin):
	list_display = ('nombre','thumbnail','precio','stock')
	list_filter = ('nombre','precio')


admin.site.register(cliente)
admin.site.register(producto,productoAdmin)
admin.site.register(categoriaProducto)