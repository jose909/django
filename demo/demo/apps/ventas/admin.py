from django.contrib import admin
from demo.apps.ventas.models import cliente,producto
from demo.apps.ventas.models import categoriaProducto


admin.site.register(cliente)
admin.site.register(producto)
admin.site.register(categoriaProducto)